import datetime
import os
import time
import json
import urllib
import warnings
import numpy
import pyqtgraph
from qtpy.QtGui import QColor, QBrush
from qtpy.QtCore import Signal, Slot, Property, QTimer, Qt, QEvent, QRect
from qtpy.QtWidgets import QToolTip
from pyqtgraph import AxisItem, PlotWidget, PlotDataItem, mkPen, ViewBox, InfiniteLine, SignalProxy, DateAxisItem, Point
from collections import OrderedDict
from typing import Optional
from utilities import colors
from multi_axis_plot import MultiAxisPlot
import bisect
from epics import pv


class NoDataError(Exception):
    """NoDataError is raised when a curve tries to perform an operation,
    but does not yet have any data."""
    pass


class BasePlotCurveItem(PlotDataItem):
    """
    BasePlotCurveItem represents a single curve in a plot.

    Parameters
    ----------
    color : QColor, optional
        The color used to draw the curve line and the symbols.
    lineStyle: int, optional
        Style of the line connecting the data points.
        Must be a value from the Qt::PenStyle enum
        (see http://doc.qt.io/qt-5/qt.html#PenStyle-enum).
    lineWidth: int, optional
        Width of the line connecting the data points.
    yAxisName: str, optional
        The name of the axis to link this curve with. Leaving it None will result in the default
        name of 'Axis 1' which may still be modified later if needed.
    **kargs: optional
        PlotDataItem keyword arguments, such as symbol and symbolSize.
    """

    REDRAW_ON_X, REDRAW_ON_Y, REDRAW_ON_EITHER, REDRAW_ON_BOTH = range(4)
    symbols = OrderedDict([('None', None),
                           ('Circle', 'o'),
                           ('Square', 's'),
                           ('Triangle', 't'),
                           ('Star', 'star'),
                           ('Pentagon', 'p'),
                           ('Hexagon', 'h'),
                           ('X', 'x'),
                           ('Diamond', 'd'),
                           ('Plus', '+')])
    lines = OrderedDict([('NoLine', Qt.NoPen),
                         ('Solid', Qt.SolidLine),
                         ('Dash', Qt.DashLine),
                         ('Dot', Qt.DotLine),
                         ('DashDot', Qt.DashDotLine),
                         ('DashDotDot', Qt.DashDotDotLine)])

    data_changed = Signal()

    def __init__(self, pvName=None, color=None, lineStyle=None, lineWidth=None, yAxisName=None, **kws):
        self._pv_name = pvName
        self._color = QColor('blue')
        self._pen = mkPen(self._color)
        if lineWidth is not None:
            self._pen.setWidth(lineWidth)
        if lineStyle is not None:
            self._pen.setStyle(lineStyle)
        kws['pen'] = self._pen
        super(BasePlotCurveItem, self).__init__(**kws)
        self.setSymbolBrush(None)
        if color is not None:
            self.color = color

        self._data_buffer = numpy.zeros((2, 4000,), dtype=float)

        if yAxisName is None:
            self._y_axis_name = 'Axis 1'
        else:
            self._y_axis_name = yAxisName

    @property
    def color_string(self) -> str:
        """
        A string representation of the color used for the curve.  This string
        will be a hex color code, like #FF00FF, or an SVG spec color name, if
        a name exists for the color.

        Returns
        -------
        str
        """
        # return str(utilities.colors.svg_color_from_hex(self.color.name(),
        return str(colors.svg_color_from_hex(self.color.name(),
                                             hex_on_fail=True))

    @color_string.setter
    def color_string(self, new_color_string):
        """
        A string representation of the color used for the curve.  This string
        will be a hex color code, like #FF00FF, or an SVG spec color name, if
        a name exists for the color.

        Parameters
        -------
        new_color_string: int
            The new string to use for the curve color.
        """
        self.color = QColor(str(new_color_string))

    @property
    def color(self):
        """
        The color used for the curve.

        Returns
        -------
        QColor
        """
        return self._color

    @color.setter
    def color(self, new_color):
        """
        The color used for the curve.

        Parameters
        -------
        new_color: QColor or str
            The new color to use for the curve.
            Strings are passed to WaveformCurveItem.color_string.
        """
        if isinstance(new_color, str):
            self.color_string = new_color
            return
        self._color = new_color
        self._pen.setColor(self._color)
        self.setPen(self._pen)
        self.setSymbolPen(self._color)

    @property
    def y_axis_name(self):
        """
        Return the name of the y-axis that this curve should be associated with. This allows us to have plots that
        contain multiple y-axes, with each curve assigned to either a unique or shared axis as needed.
        Returns
        -------
        str
        """
        return self._y_axis_name

    @y_axis_name.setter
    def y_axis_name(self, axis_name):
        """
        Set the name of the y-axis that should be associated with this curve.
        Parameters
        ----------
        axis_name: str
        """
        self._y_axis_name = axis_name

    @property
    def pv_name(self) -> str:
        """
        Return the name of the PV that this curve should be associated with.
        Returns
        -------
        str
        """
        return self._pv_name

    @pv_name.setter
    def pv_name(self, pv_name):
        """
        Set the name of the PV that should be associated with this curve.
        Parameters
        ----------
        pv_name: str
        """
        self._pv_name = pv_name

    @property
    def lineStyle(self):
        """
        Return the style of the line connecting the data points.
        Must be a value from the Qt::PenStyle enum
        (see http://doc.qt.io/qt-5/qt.html#PenStyle-enum).

        Returns
        -------
        int
        """
        return self._pen.style()

    @lineStyle.setter
    def lineStyle(self, new_style):
        """
        Set the style of the line connecting the data points.
        Must be a value from the Qt::PenStyle enum
        (see http://doc.qt.io/qt-5/qt.html#PenStyle-enum).

        Parameters
        -------
        new_style: int
        """
        if new_style in self.lines.values():
            self._pen.setStyle(new_style)
            self.setPen(self._pen)

    @property
    def lineWidth(self):
        """
        Return the width of the line connecting the data points.

        Returns
        -------
        int
        """
        return self._pen.width()

    @lineWidth.setter
    def lineWidth(self, new_width):
        """
        Set the width of the line connecting the data points.

        Parameters
        -------
        new_width: int
        """
        self._pen.setWidth(int(new_width))
        self.setPen(self._pen)

    @property
    def symbol(self):
        """
        The single-character code for the symbol drawn at each datapoint.

        See the documentation for pyqtgraph.PlotDataItem for possible values.

        Returns
        -------
        str or None
        """
        return self.opts['symbol']

    @symbol.setter
    def symbol(self, new_symbol):
        """
        The single-character code for the symbol drawn at each datapoint.

        See the documentation for pyqtgraph.PlotDataItem for possible values.

        Parameters
        -------
        new_symbol: str or None
        """
        if new_symbol in self.symbols.values():
            self.setSymbol(new_symbol)
            self.setSymbolPen(self._color)

    @property
    def symbolSize(self):
        """
        Return the size of the symbol to represent the data.

        Returns
        -------
        int
        """
        return self.opts['symbolSize']

    @symbolSize.setter
    def symbolSize(self, new_size):
        """
        Set the size of the symbol to represent the data.

        Parameters
        -------
        new_size: int
        """
        self.setSymbolSize(int(new_size))

    @property
    def data_buffer(self):
        """
        Return the archived data_buffer of the PV that this curve should be associated with.
        Returns
        -------
        2-D array
        """
        return self._data_buffer

    @data_buffer.setter
    def data_buffer(self, data_buffer):
        """
        Set the data_buffer that should be associated with this curve.
        Parameters
        ----------
        2-D array
        """
        self._data_buffer = data_buffer

    def to_dict(self):
        """
        Returns an OrderedDict representation with values for all properties
        needed to recreate this curve.

        Returns
        -------
        OrderedDict
        """
        return OrderedDict([("name", self.name()),
                            ("pvName", self.pv_name),
                            ("color", self.color_string),
                            ("lineStyle", self.lineStyle),
                            ("lineWidth", self.lineWidth),
                            ("symbol", self.symbol),
                            ("symbolSize", self.symbolSize),
                            ("yAxisName", self.y_axis_name)])

    def close(self):
        pass

    def setArchiverData(self, start_time, end_time, strategy='lastSample'):
        start_time_obj = datetime.datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ")
        end_time_obj = datetime.datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%SZ")
        interval_sec = (end_time_obj - start_time_obj).total_seconds()
        bin_size = int(interval_sec / 7200)
        if bin_size <= 1:
            url_string = os.environ.get(
                'ARCHIVER_URL').__str__() + f":17668/retrieval/data/getData.json?pv={self.pv_name}&from={start_time}&to={end_time}&fetchLatestMetadata=true"
        else:
            url_string = os.environ.get(
                'ARCHIVER_URL').__str__() + f":17668/retrieval/data/getData.json?pv={strategy}_{bin_size}({self.pv_name})&from={start_time}&to={end_time}&fetchLatestMetadata=true"

        req = urllib.request.urlopen(url_string)
        data = json.load(req)
        secs = [x['secs'] for x in data[0]['data']]
        vals = [x['val'] for x in data[0]['data']]
        nanos = [x['nanos'] for x in data[0]['data']]
        if secs:
            vals = vals[1:]
            float_nanos = (numpy.array(nanos) * (1e-6))[1:]
            secs = secs[1:] + numpy.round(float_nanos) * (1e-3)
        # print(secs)
        # print(vals)
        # print(vals.__len__())
        self.setData(x=secs, y=vals, stepMode="right", connect="all")

    def getArchiverData(self, start_time, end_time, strategy='lastSample'):
        start_time_obj = datetime.datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ")
        end_time_obj = datetime.datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%SZ")
        interval_sec = (end_time_obj - start_time_obj).total_seconds()
        bin_size = int(interval_sec / 7200)
        if bin_size <= 1:
            url_string = os.environ.get(
                'ARCHIVER_URL').__str__() + f":17668/retrieval/data/getData.json?pv={self.pv_name}&from={start_time}&to={end_time}&fetchLatestMetadata=true"
        else:
            url_string = os.environ.get(
                'ARCHIVER_URL').__str__() + f":17668/retrieval/data/getData.json?pv={strategy}_{bin_size}({self.pv_name})&from={start_time}&to={end_time}&fetchLatestMetadata=true"

        req = urllib.request.urlopen(url_string)
        data = json.load(req)
        secs = [x['secs'] for x in data[0]['data']]
        vals = [x['val'] for x in data[0]['data']]
        nanos = [x['nanos'] for x in data[0]['data']]
        vals = vals[1:]

        float_nanos = (numpy.array(nanos) * (1e-6))[1:]
        secs = secs[1:] + numpy.round(float_nanos) * (1e-3)
        return secs, vals


    def getCorrelatorData(self, start_time, end_time, strategy='mean'):

        start_time_obj = datetime.datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ")
        end_time_obj = datetime.datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%SZ")
        interval_sec = (end_time_obj - start_time_obj).total_seconds()
        bin_size = int(interval_sec / 7200)
        if bin_size <= 1:
            bin_size = 1
        url_string = os.environ.get(
            'ARCHIVER_URL').__str__() + f":17668/retrieval/data/getData.json?pv={strategy}_{bin_size}({self.pv_name})&from={start_time}&to={end_time}&fetchLatestMetadata=true"

        req = urllib.request.urlopen(url_string)
        data = json.load(req)
        secs = [x['secs'] for x in data[0]['data']]
        vals = [x['val'] for x in data[0]['data']]
        vals = vals[1:]
        return secs, vals


class BasePlotAxisItem(AxisItem):
    """
    BasePlotAxisItem represents a single axis in a plot.

    Parameters
    ----------
    name: str
        The name of the axis
    orientation: str, optional
        The orientation of this axis. The default for this value is 'left'. Must be set to either 'right', 'top',
        'bottom', or 'left'. See: https://pyqtgraph.readthedocs.io/en/latest/graphicsItems/axisitem.html
    label: str, optional
        The label to be displayed along the axis
    minRange: float, optional
        The minimum value to be displayed on this axis
    maxRange: float, optional
        The maximum value to be displayed on this axis
    autoRange: bool, optional
        Whether or not this axis should automatically update its range as it receives new data
    logMode: bool, optional
        If true, this axis will start in logarithmic mode, will be linear otherwise
    **kws: optional
        Extra arguments for CSS style options for this axis
    """

    axis_orientations = OrderedDict([('Left', 'left'),
                                     ('Right', 'right')])

    def __init__(self, name, orientation='left', label=None, minRange=-1.0,
                 maxRange=1.0, autoRange=True, logMode=False, **kws):
        super(BasePlotAxisItem, self).__init__(orientation, **kws)

        self._name = name
        self._orientation = orientation
        self._label = label
        self._min_range = minRange
        self._max_range = maxRange
        self._auto_range = autoRange
        self._log_mode = logMode

    @property
    def name(self):
        """
        Return the name of the axis

        Returns
        -------
        str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Set the name of the axis

        Parameters
        ----------
        name: str
        """
        self._name = name

    @property
    def orientation(self):
        """
        Return the orientation of the y-axis this curve is associated with. Will be 'left', 'right', 'bottom', or 'top'
        See: https://pyqtgraph.readthedocs.io/en/latest/graphicsItems/axisitem.html

        Returns
        -------
        str
        """
        return self._orientation

    @orientation.setter
    def orientation(self, orientation):
        """
        Set the orientation of the y-axis this curve is associated with. Must be 'left', 'right', 'bottom', or 'top'

        Parameters
        ----------
        orientation: str
        """
        self._orientation = orientation

    @property
    def label_text(self) -> str:
        """ Return the label to be displayed along this axis. """
        return self._label

    @label_text.setter
    def label_text(self, label: str):
        """ Set the label to be displayed along this axis """
        self._label = label

    @property
    def min_range(self):
        """
        Return the minimum range displayed on this axis

        Returns
        -------
        float
        """
        return self._min_range

    @min_range.setter
    def min_range(self, min_range):
        """
        Set the minimum range for this axis

        Parameters
        ----------
        min_range: float
        """
        self._min_range = min_range

    @property
    def max_range(self):
        """
        Return the maximum range displayed on this axis

        Returns
        -------
        float
        """
        return self._max_range

    @max_range.setter
    def max_range(self, max_range):
        """
        Set the maximum range for this axis

        Parameters
        ----------
        max_range: float
        """
        self._max_range = max_range

    @property
    def auto_range(self):
        """
        Return whether or not this axis should automatically update its range when receiving new data

        Returns
        -------
        bool
        """
        return self._auto_range

    @auto_range.setter
    def auto_range(self, auto_range):
        """
        Set whether or not this axis should automatically update its range when receiving new data

        Parameters
        ----------
        auto_range: bool
        """
        self._auto_range = auto_range

    @property
    def log_mode(self):
        """
        Return whether or not this axis is using logarithmic mode

        Returns
        -------
        bool
        """
        return self._log_mode

    @log_mode.setter
    def log_mode(self, log_mode):
        """
        Set whether or not this axis is using logarithmic mode

        Parameters
        ----------
        log_mode: bool
        """
        self._log_mode = log_mode

    def to_dict(self):
        """
        Returns an OrderedDict representation with values for all properties
        needed to recreate this axis.

        Returns
        -------
        OrderedDict
        """
        return OrderedDict([("name", self._name),
                            ("orientation", self._orientation),
                            ("label", self._label),
                            ("minRange", self._min_range),
                            ("maxRange", self._max_range),
                            ("autoRange", self._auto_range),
                            ("logMode", self._log_mode)])


class TimeAxisItem(AxisItem):
    """
    TimeAxisItem formats a unix time axis into a human-readable format.
    """

    def __init__(self, *args, **kwargs):
        super(TimeAxisItem, self).__init__(*args, **kwargs)
        self.enableAutoSIPrefix(False)
        self.setStyle(autoReduceTextSpace=True)

    def tickStrings(self, values, scale, spacing):
        strings = []
        for val in values:
            strings.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(val)))
        return strings


class BasePlot(PlotWidget):
    crosshair_position_updated = Signal(float, float)

    def __init__(self, parent=None, background='default', axisItems=None):
        # First create a custom MultiAxisPlot to pass to the base PlotWidget class to support multiple y axes. Note
        # that this plot will still function just fine in the case the user doesn't need additional y axes.
        plotItem = MultiAxisPlot(axisItems=axisItems)

        if axisItems is None or 'left' not in axisItems:
            # The pyqtgraph PlotItem.setAxisItems() will always add an an AxisItem called left whether you asked
            # it to or not. This will clear it if not specifically requested.
            plotItem.removeAxis('left')
        super(BasePlot, self).__init__(parent=parent, background=background, plotItem=plotItem)

        self.plotItem = plotItem
        self.plotItem.hideButtons()
        self._auto_range_x = None
        self.setAutoRangeX(True)
        self._auto_range_y = None
        self.setAutoRangeY(True)
        self._min_x = 0.0
        self._max_x = 1.0
        self._min_y = 0.0
        self._max_y = 1.0
        self._show_x_grid = None
        self.setShowXGrid(True)
        self._show_y_grid = None
        self.setShowYGrid(True)

        self._show_right_axis = False

        self._axes = []
        self._curves = []
        self._x_labels = []
        self._y_labels = []
        self._title = None
        self._show_legend = False
        self._legend = self.addLegend()
        self._legend.hide()

        # Drawing crosshair on the ViewBox
        self.vertical_crosshair_line = None
        self.horizontal_crosshair_line = None
        self.crosshair_movement_proxy = None

        self.cursorlabel = pyqtgraph.TextItem(anchor=(0, 0))
        self.addItem(self.cursorlabel)

        self.redraw_timer = QTimer(self)
        self.redraw_timer.timeout.connect(self.redrawPlot)
        self.redraw_timer.setInterval(1000)  # 1000ms

        # Mouse mode to 1 button (left button draw rectangle for zoom)
        self.plotItem.getViewBox().setMouseMode(ViewBox.RectMode)

        if self.getAxis('bottom') is not None:
            # Disables unexpected axis tick behavior described here:
            # https://pyqtgraph.readthedocs.io/en/latest/graphicsItems/axisitem.html
            self.getAxis('bottom').enableAutoSIPrefix(False)

    def eventFilter(self, obj, event):
        ret = super(BasePlot, self).eventFilter(obj, event)

        if event.type() == QEvent.Enter:
            QToolTip.showText(
                self.mapToGlobal(self.rect().center()),
                'Edit plot curves via Right-Click and select "Edit Curves..."',
                self,
                QRect(0, 0, 200, 100),
                4000)

        return ret

    def addYChannel(self, pvName=None, name=None, color=None,
                    lineStyle=None, lineWidth=None, symbol=None,
                    symbolSize=None, yAxisName=None):
        """
               Add a new curve to the plot.  In addition to the arguments below,
               all other keyword arguments are passed to the underlying
               pyqtgraph.PlotDataItem used to draw the curve.

               Parameters
               ----------
               pvName: str
                   The name for the channel for the curve.
               name: str, optional
                   A name for this curve.  The name will be used in the plot legend.
               color: str or QColor, optional
                   A color for the line of the curve.  If not specified, the plot will
                   automatically assign a unique color from a set of default colors.
               lineStyle: int, optional
                   Style of the line connecting the data points.
                   0 means no line (scatter plot).
               lineWidth: int, optional
                   Width of the line connecting the data points.
               symbol: str or None, optional
                   Which symbol to use to represent the data.
               symbolSize: int, optional
                   Size of the symbol.
               yAxisName : str, optional
                   The name of the y axis to associate with this curve. Will be created if it
                   doesn't yet exist
               """
        plot_opts = {}
        plot_opts['symbol'] = symbol
        if symbolSize is not None:
            plot_opts['symbolSize'] = symbolSize
        if lineStyle is not None:
            plot_opts['lineStyle'] = lineStyle
        if lineWidth is not None:
            plot_opts['lineWidth'] = lineWidth
        if pvName is not None:
            plot_opts['pvName'] = pvName

        curve = BasePlotCurveItem(pv_name=pvName, name=name, color=color,
                                  yAxisName=yAxisName, **plot_opts)
        self.addCurve(curve, curve_color=color, y_axis_name=yAxisName)

    def addCurve(self, plot_data_item, curve_color=None, y_axis_name=None):
        """
        Adds a curve to this plot. 

        If the y axis parameters are specified, either link this curve to an
        existing axis if that axis is already part of this plot, or create a
        new one and link the curve to it.

        Parameters
        ----------
        plot_data_item: BasePlotCurveItem
            The curve to add to this plot
        curve_color: QColor, optional
            The color to draw the curve and axis label in
        y_axis_name: str, optional
            The name of the axis to link the curve with. If this is the first
            time seeing this name, then a new axis will be created for it.
        """
        if curve_color is None:
            # curve_color = utilities.colors.default_colors[
            #    len(self._curves) % len(utilities.colors.default_colors)]
            curve_color = colors.default_colors[
                len(self._curves) % len(colors.default_colors)]
            plot_data_item.color_string = curve_color
        self._curves.append(plot_data_item)
        if y_axis_name is None:
            if 'Axis 1' not in self.plotItem.axes:
                # self.plotItem.setAxisItems()
                # self.addItem(plot_data_item)
                self.addAxis(plot_data_item=plot_data_item, name='Axis 1', orientation='left')
                # self.addAxis(plot_data_item=plot_data_item, name='left', orientation='left')
            else:
                # self.plotItem.linkDataToAxis(plot_data_item, 'left')
                self.plotItem.linkDataToAxis(plot_data_item, 'Axis 1')

        elif y_axis_name in self.plotItem.axes:
            # If the user has chosen an axis that already exists for this curve, simply link the data to that axis
            self.plotItem.linkDataToAxis(plot_data_item, y_axis_name)
        else:
            # Otherwise we create a brand new axis for this data
            self.addAxis(plot_data_item=plot_data_item, name=y_axis_name, orientation='left')

    def addAxis(self, plot_data_item: BasePlotCurveItem, name: str, orientation: str,
                label: Optional[str] = None, min_range: Optional[float] = -1.0,
                max_range: Optional[float] = 1.0, enable_auto_range: Optional[bool] = True,
                log_mode: Optional[bool] = False):
        """
        Create an AxisItem with the input name and orientation, and add it to
        this plot.

        Parameters
        ----------
        plot_data_item: BasePlotCurveItem
            The curve that will be linked with this new axis
        name: str
            The name that will be assigned to this axis
        orientation: str
            The orientation of this axis, must be in 'left' or 'right'
        label: str, optional
            The label to be displayed along this axis
        min_range: float
            The minimum range to display on the axis
        max_range: float
            The maximum range to display on the axis
        enable_auto_range: bool, optional
            Whether or not to use autorange for this axis. Min and max range will not be respected
            when data goes out of range if this is set to True
        log_mode: bool, optional
            Whether or not this axis should start out in logarithmic mode.

        Raises
        ------
        Exception
            Raised by PyQtGraph if the orientation is not in 'left' or 'right'
        """
        if name in self.plotItem.axes:
            return

        axis = BasePlotAxisItem(name=name, orientation=orientation, label=label, minRange=min_range,
                                maxRange=max_range, autoRange=enable_auto_range, logMode=log_mode)
        axis.setLabel(text=label)
        axis.enableAutoSIPrefix(False)
        if plot_data_item is not None:
            plot_data_item.setLogMode(False, log_mode)
        axis.setLogMode(log_mode)
        self._axes.append(axis)
        # If the x axis is just timestamps, we don't want autorange on the x axis
        setXLink = hasattr(self, '_plot_by_timestamps') and self._plot_by_timestamps
        self.plotItem.addAxis(axis, name=name, plotDataItem=plot_data_item, setXLink=setXLink,
                              enableAutoRangeX=self.getAutoRangeX(), enableAutoRangeY=enable_auto_range,
                              minRange=min_range, maxRange=max_range)

    def removeCurve(self, plot_item):
        if plot_item.y_axis_name in self.plotItem.axes:
            self.plotItem.unlinkDataFromAxis(plot_item.y_axis_name)

        self.removeItem(plot_item)
        self._curves.remove(plot_item)

    def removeAxisAtIndex(self, axis_index):
        axis = self._axes[axis_index]
        self.plotItem.removeAxis(axis.name)
        self._axes.remove(axis)

    def removeCurveWithName(self, name):
        for curve in self._curves:
            if curve.name() == name:
                self.removeCurve(curve)

    def removeCurveAtIndex(self, index):
        curve_to_remove = self._curves[index]
        self.removeCurve(curve_to_remove)

    def setCurveAtIndex(self, index, new_curve):
        old_curve = self._curves[index]
        self._curves[index] = new_curve
        # self._legend.addItem(new_curve, new_curve.name())
        self.removeCurve(old_curve)

    def curveAtIndex(self, index):
        return self._curves[index]

    def curves(self):
        return self._curves

    def getCurves(self):
        """
        Dump the current list of curves and each curve's settings into a list
        of JSON-formatted strings.

        Returns
        -------
        settings : list
            A list of JSON-formatted strings, each containing a curve's
            settings
        """
        return [json.dumps(curve.to_dict()) for curve in self._curves]

    def setCurves(self, new_list):
        """
        Add a list of curves into the graph.

        Parameters
        ----------
        new_list : list
            A list of JSON-formatted strings, each contains a curve and its
            settings
        """
        try:
            new_list = [json.loads(str(i)) for i in new_list]
        except ValueError as e:
            print("Error parsing curve json data: {}".format(e))
            return
        self.clearCurves()

        for d in new_list:
            color = d.get('color')
            if color:
                color = QColor(color)
            self.addYChannel(pvName=d.get('pvName'),
                             name=d.get('name'),
                             color=color,
                             lineStyle=d.get('lineStyle'),
                             lineWidth=d.get('lineWidth'),
                             symbol=d.get('symbol'),
                             symbolSize=d.get('symbolSize'),
                             yAxisName=d.get('yAxisName'))

    def clearCurves(self):
        """
        Remove all curves from the graph.
        """
        self.clear1()

    curves = Property("QStringList", getCurves, setCurves, designable=False)

    def clear1(self):
        '''
        legend_items = [label.text for (sample, label) in self._legend.items]
        for item in legend_items:
            self._legend.removeItem(item)
        '''

        # print(self.plotItem.items)
        # for i in self.plotItem.items:
        # print(i._pv_name)
        # print(i)

        self.plotItem.clear()
        self._curves = []

    def clearAxes(self):
        """ Clear out any added axes on this plot """
        # for axis in self._axes:
        #    axis.deleteLater()
        self.plotItem.clearAxes()
        self._axes = []
        # print(self.plotItem.axes)

    def getShowXGrid(self):
        return self._show_x_grid

    def setShowXGrid(self, value, alpha=None):
        self._show_x_grid = value
        self.showGrid(x=self._show_x_grid, alpha=alpha)

    def resetShowXGrid(self):
        self.setShowXGrid(False)

    showXGrid = Property("bool", getShowXGrid, setShowXGrid, resetShowXGrid)

    def getShowYGrid(self):
        return self._show_y_grid

    def setShowYGrid(self, value, alpha=None):
        self._show_y_grid = value
        self.showGrid(y=self._show_y_grid, alpha=alpha)

    def resetShowYGrid(self):
        self.setShowYGrid(False)

    showYGrid = Property("bool", getShowYGrid, setShowYGrid, resetShowYGrid)

    def getBackgroundColor(self):
        return self.backgroundBrush().color()

    def setBackgroundColor(self, color):
        if self.backgroundBrush().color() != color:
            self.setBackgroundBrush(QBrush(color))

    backgroundColor = Property(QColor, getBackgroundColor, setBackgroundColor)

    def getAxisColor(self):
        return self.getAxis('bottom')._pen.color()

    def setAxisColor(self, color):
        for axis in self.plotItem.axes.values():
            axis['item'].setPen(color)

    axisColor = Property(QColor, getAxisColor, setAxisColor)

    def getYAxes(self):
        """
        Dump the current list of axes and each axis's settings into a list
        of JSON-formatted strings.

        Returns
        -------
        settings : list
            A list of JSON-formatted strings, each containing a curve's
            settings
        """
        return [json.dumps(axis.to_dict()) for axis in self._axes]

    def setYAxes(self, new_list):
        """
        Add a list of axes into the graph.

        Parameters
        ----------
        new_list : list
            A list of JSON-formatted strings, each contains an axis and its
            settings
        """
        try:
            new_list = [json.loads(str(i)) for i in new_list]
        except ValueError as e:
            print("Error parsing curve json data: {}".format(e))
            return
        self.clearAxes()
        for d in new_list:
            self.addAxis(plot_data_item=None, name=d.get('name'), orientation=d.get('orientation'),
                         label=d.get('label'), min_range=d.get('minRange'), max_range=d.get('maxRange'),
                         enable_auto_range=d.get('autoRange'), log_mode=d.get('logMode'))

        if 'bottom' in self.plotItem.axes:
            # Ensure the added y axes get the color that was set
            self.setAxisColor(self.getAxis('bottom')._pen.color())
        if self.getShowYGrid() or self.getShowXGrid():
            self.plotItem.updateGrid()

    yAxes = Property("QStringList", getYAxes, setYAxes, designable=False)

    def getBottomAxisLabel(self):
        return self.getAxis('bottom').labelText

    def getShowRightAxis(self):
        """
        Provide whether the right y-axis is being shown.

        Returns
        -------
        bool
            True if the graph shows the right y-axis. False if not.
        """
        return self._show_right_axis

    def setShowRightAxis(self, show):
        """
        Set whether the graph should show the right y-axis.

        Parameters
        ----------
        show : bool
            True for showing the right axis; False is for not showing.
        """
        if show:
            self.showAxis("right")
        else:
            self.hideAxis("right")
        self._show_right_axis = show

    showRightAxis = Property("bool", getShowRightAxis, setShowRightAxis)

    def getPlotTitle(self):
        if self._title is None:
            return ""
        return str(self._title)

    def setPlotTitle(self, value):
        self._title = str(value)
        if len(self._title) < 1:
            self._title = None
        self.setTitle(self._title)

    def resetPlotTitle(self):
        self._title = None
        self.setTitle(self._title)

    title = Property(str, getPlotTitle, setPlotTitle, resetPlotTitle)

    def getXLabels(self):
        return self._x_labels

    def setXLabels(self, labels):
        if self._x_labels != labels:
            self._x_labels = labels
            label = ""
            if len(self._x_labels) > 0:
                # Hardcoded for now as we only have one axis
                label = self._x_labels[0]
            self.setLabel("bottom", text=label)

    def resetXLabels(self):
        self._x_labels = []
        self.setLabel("bottom", text="")

    xLabels = Property("QStringList", getXLabels, setXLabels, resetXLabels)

    def getYLabels(self):
        warnings.warn("Y Labels should be retrieved from the AxisItem. See: AxisItem.label or AxisItem.labelText"
                      "Example: self.getAxis('Axis Name').labelText",
                      DeprecationWarning,
                      stacklevel=2)
        return self._y_labels

    def setYLabels(self, labels):
        warnings.warn("Y Labels should now be set on the AxisItem itself. See: AxisItem.setLabel() "
                      "Example: self.getAxis('Axis Name').setLabel('Label Name')",
                      DeprecationWarning,
                      stacklevel=2)
        if self._y_labels != labels:
            self._y_labels = labels
            label = ""
            if len(self._y_labels) > 0:
                # Hardcoded for now as we only have one axis
                label = self._y_labels[0]
            if 'left' in self.plotItem.axes:
                self.setLabel("left", text=label)

    def resetYLabels(self):
        warnings.warn("Y Labels should now be set on the AxisItem itself. See: AxisItem.setLabel() "
                      "Example: self.getAxis('Axis Name').setLabel('')",
                      DeprecationWarning,
                      stacklevel=2)
        self._y_labels = []
        self.setLabel("left", text="")

    def getShowLegend(self):
        """
        Check if the legend is being shown.

        Returns
        -------
        bool
            True if the legend is displayed on the graph; False if not.
        """
        return self._show_legend

    def setShowLegend(self, value):
        """
        Set to display the legend on the graph.

        Parameters
        ----------
        value : bool
            True to display the legend; False is not.
        """
        self._show_legend = value
        if self._show_legend:
            if self._legend is None:
                self._legend = self.addLegend()
            else:
                self._legend.show()
        else:
            if self._legend is not None:
                self._legend.hide()

    def resetShowLegend(self):
        """
        Reset the legend display status to hidden.
        """
        self.setShowLegend(False)

    showLegend = Property(bool, getShowLegend, setShowLegend, resetShowLegend)

    def getAutoRangeX(self):
        return self._auto_range_x

    def setAutoRangeX(self, value):
        self._auto_range_x = value
        if self._auto_range_x:
            self.plotItem.enableAutoRange(ViewBox.XAxis, enable=self._auto_range_x)

    def resetAutoRangeX(self):
        self.setAutoRangeX(True)

    def getAutoRangeY(self):
        return self._auto_range_y

    def setAutoRangeY(self, value):
        self._auto_range_y = value
        if self._auto_range_y:
            self.plotItem.enableAutoRange(ViewBox.YAxis, enable=self._auto_range_y)

    def resetAutoRangeY(self):
        self.setAutoRangeY(True)

    def getMinXRange(self):
        """
        Minimum X-axis value visible on the plot.

        Returns
        -------
        float
        """
        return self.plotItem.viewRange()[0][0]

    def setMinXRange(self, new_min_x_range):
        """
        Set the minimum X-axis value visible on the plot.

        Parameters
        -------
        new_min_x_range : float
        """
        if self._auto_range_x:
            return
        self._min_x = new_min_x_range
        self.plotItem.setXRange(self._min_x, self._max_x, padding=0)

    def getMaxXRange(self):
        """
        Maximum X-axis value visible on the plot.

        Returns
        -------
        float
        """
        return self.plotItem.viewRange()[0][1]

    def setMaxXRange(self, new_max_x_range):
        """
        Set the Maximum X-axis value visible on the plot.

        Parameters
        -------
        new_max_x_range : float
        """
        if self._auto_range_x:
            return

        self._max_x = new_max_x_range
        self.plotItem.setXRange(self._min_x, self._max_x, padding=0)

    def getMinYRange(self):
        """
        Minimum Y-axis value visible on the plot.

        Returns
        -------
        float
        """
        return self.plotItem.viewRange()[1][0]

    def setMinYRange(self, new_min_y_range):
        """
        Set the minimum Y-axis value visible on the plot.

        Parameters
        -------
        new_min_y_range : float
        """
        if self._auto_range_y:
            return

        self._min_y = new_min_y_range
        self.plotItem.setYRange(self._min_y, self._max_y, padding=0)

    def getMaxYRange(self):
        """
        Maximum Y-axis value visible on the plot.

        Returns
        -------
        float
        """
        return self.plotItem.viewRange()[1][1]

    def setMaxYRange(self, new_max_y_range):
        """
        Set the maximum Y-axis value visible on the plot.

        Parameters
        -------
        new_max_y_range : float
        """
        if self._auto_range_y:
            return

        self._max_y = new_max_y_range
        self.plotItem.setYRange(self._min_y, self._max_y, padding=0)

    @Property(bool)
    def mouseEnabledX(self):
        """
        Whether or not mouse interactions are enabled for the X-axis.

        Returns
        -------
        bool
        """
        return self.plotItem.getViewBox().state['mouseEnabled'][0]

    @mouseEnabledX.setter
    def mouseEnabledX(self, x_enabled):
        """
        Whether or not mouse interactions are enabled for the X-axis.

        Parameters
        -------
        x_enabled : bool
        """
        self.plotItem.setMouseEnabled(x=x_enabled)

    @Property(bool)
    def mouseEnabledY(self):
        """
        Whether or not mouse interactions are enabled for the Y-axis.

        Returns
        -------
        bool
        """
        return self.plotItem.getViewBox().state['mouseEnabled'][1]

    @mouseEnabledY.setter
    def mouseEnabledY(self, y_enabled):
        """
        Whether or not mouse interactions are enabled for the Y-axis.

        Parameters
        -------
        y_enabled : bool
        """
        self.plotItem.setMouseEnabled(y=y_enabled)

    @Property(int)
    def maxRedrawRate(self):
        """
        The maximum rate (in Hz) at which the plot will be redrawn.
        The plot will not be redrawn if there is not new data to draw.

        Returns
        -------
        int
        """
        return self._redraw_rate

    @maxRedrawRate.setter
    def maxRedrawRate(self, redraw_rate):
        """
        The maximum rate (in Hz) at which the plot will be redrawn.
        The plot will not be redrawn if there is not new data to draw.

        Parameters
        -------
        redraw_rate : int
        """
        self._redraw_rate = redraw_rate
        self.redraw_timer.setInterval(int((1.0 / self._redraw_rate) * 1000))

    def pausePlotting(self):
        self.redraw_timer.stop() if self.redraw_timer.isActive() else self.redraw_timer.start()
        return self.redraw_timer.isActive()

    def redrawPlot(self):
        """
        Used to plot live curves. Redraw the curves. Delete the first data of the data_buffer and add the PV value from
        EPICS channel as the last data of the data_buffer

        for curve in self._curves:
            curve.redrawCurve()
        """
        start_time = "2024-07-09T7:20:00Z"
        end_time = "2024-07-09T7:25:00Z"
        for curve in self._curves:
            # (secs, vals) = curve.getArchiverData(start_time, end_time)
            curve.data_buffer = numpy.roll(curve.data_buffer, -1)
            bufferSize = curve.data_buffer[0].__len__()
            curve.data_buffer[0, bufferSize - 1] = round(time.time() * 1000) / 1000  # ms
            curve.data_buffer[1, bufferSize - 1] = pv.PV(curve.pv_name).get()
            curve.setData(x=curve.data_buffer[0], y=curve.data_buffer[1], stepMode="right", connect="all")

    def mouseMoved(self, evt):
        """
        A handler for the crosshair feature. Every time the mouse move, the mouse coordinates are updated, and the
        horizontal and vertical hairlines will be redrawn at the new coordinate. It will display
        the x- and y- values to update on the UI.

        Parameters
        -------
        evt: MouseEvent
            The mouse event type, from which the mouse coordinates are obtained.
        """

        pos = evt[0]

        if self.sceneBoundingRect().contains(pos):
            # mouse_point = self.getViewBox().mapSceneToView(pos)
            time = 0.0
            text = ''
            htmlStr = ''
            if self._axes:
                # mouse_point = self._axes.__getitem__(0).linkedView().mapSceneToView(pos)
                time = self._axes.__getitem__(0).linkedView().mapSceneToView(pos).x()
                time_obj = datetime.datetime.fromtimestamp(time)
                time_str = time_obj.strftime("%Y-%m-%d %H:%M:%S")
                text = text + 'Time=' + time_str
                htmlStr = htmlStr + "<span style='font-size:20px; color:white; background-color: gray'>" + "Time=" + time_str + '<br>' + "</span>"
                view = self._axes.__getitem__(-1).linkedView()
                self.cursorlabel.setParentItem(view)
                # point=QPointF(mouse_point.x(), mouse_point.y())
                # self.cursorlabel.setPos(view.mapViewToScene(point))

                self.cursorlabel.setPos(pos)

            curves = self.plotItem.curves
            for curve in curves:
                xdata = curve.xData
                ydata = curve.yData
                if xdata is not None:
                    if time >= xdata[-1]:
                        return False
                    if time <= xdata[0]:
                        return False
                    num = bisect.bisect_left(xdata, time)
                    before = xdata[num - 1]
                    after = xdata[num]
                    if after - time < time - before:
                        text = text + ',' + curve.pv_name + '=' + str(ydata[num])
                        # htmlStr = htmlStr + "<span style='background-color: grey;color: " + str(curve.color_string) +";'>" + curve.pv_name +"="+str(ydata[num])+"<br>"+ "</span>"
                        htmlStr = htmlStr + "<span style='font-size:20px; color:black; background-color: " + str(
                            curve.color_string) + ";'>" + curve.pv_name + "=" + str(ydata[num]) + "<br>" + "</span>"
                        # print(ydata[num])
                    else:
                        # print(ydata[num-1])
                        text = text + ',' + curve.pv_name + '=' + str(ydata[num - 1])
                        htmlStr = htmlStr + "<span style='font-size:20px; color:black; background-color: " + str(
                            curve.color_string) + ";'>" + curve.pv_name + "=" + str(ydata[num - 1]) + "<br>" + "</span>"

                self.cursorlabel.setHtml(htmlStr)
                # self.addItem(self.cursorlabel)
                # self.cursorlabel.setPos(pos)

            '''
            for axis in self._axes:
                mouse_point = axis.linkedView().mapSceneToView(pos)
                time = axis.linkedView().mapSceneToView(pos).x()
            '''
            # for view in self.plotItem.stackedViews:
            #    print(view.name)
            # print(self.plotItem.getViewBox().getViewBox())
            # mouse_point = self.plotItem.getViewBox().mapSceneToView(pos)
            # self.vertical_crosshair_line.setPos(mouse_point.x())
            # self.horizontal_crosshair_line.setPos(mouse_point.y())
            # print(mouse_point.x())
            label = ''
            # print(self.plotItem.curves)
            # self.crosshair_position_updated.emit(mouse_point.x(), mouse_point.y())


    def enableCrosshair(self, is_enabled, vertical_angle=90, horizontal_angle=0,
                        vertical_movable=False, horizontal_movable=False):
        """
        Enable the crosshair to be drawn on the ViewBox.

        Parameters
        ----------
        is_enabled : bool
            True is to draw the crosshair, False is to not draw.
        starting_x_pos : float
            The x coordinate where to start the vertical crosshair line.
        starting_y_pos : float
            The y coordinate where to start the horizontal crosshair line.
        vertical_angle : float
            The angle to tilt the vertical crosshair line. Default at 90 degrees.
        horizontal_angle
            The angle to tilt the horizontal crosshair line. Default at 0 degrees.
        vertical_movable : bool
            True if the vertical line can be moved by the user; False is not.
        horizontal_movable
            False if the horizontal line can be moved by the user; False is not.
        """
        if is_enabled:

            self.vertical_crosshair_line = InfiniteLine(angle=vertical_angle,
                                                        movable=vertical_movable)
            self.horizontal_crosshair_line = InfiniteLine(angle=horizontal_angle,
                                                          movable=horizontal_movable)

            self.plotItem.addItem(self.vertical_crosshair_line)
            self.plotItem.addItem(self.horizontal_crosshair_line)
            self.crosshair_movement_proxy = SignalProxy(self.plotItem.scene().sigMouseMoved, rateLimit=60,
                                                        slot=self.mouseMoved)
        else:
            if self.vertical_crosshair_line:
                self.plotItem.removeItem(self.vertical_crosshair_line)
            if self.horizontal_crosshair_line:
                self.plotItem.removeItem(self.horizontal_crosshair_line)
            if self.crosshair_movement_proxy:
                # self.crosshair_movement_proxy.disconnect()
                proxy = self.crosshair_movement_proxy
                proxy.block = True
                try:
                    proxy.signal.disconnect(proxy.signalReceived)
                    proxy.sigDelayed.disconnect(proxy.slot)
                except:
                    pass
