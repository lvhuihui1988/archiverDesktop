import json
import re
import time
import urllib.request
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import sys
import os
import numpy

from PyQt5.QtCore import pyqtSignal, QDateTime, QSize
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QColor, QBrush, QTextDocument, QMovie, QTextItem
from PyQt5.QtWidgets import QDialog, QMainWindow, QFileDialog, QMessageBox, QProgressDialog, QGridLayout
from pyqtgraph import PlotWidget, AxisItem, DateAxisItem, GraphicsLayoutWidget, GraphicsWindow
import pandas as pd
import pyqtgraph

from baseplot_curve_editor import BasePlotCurveEditor, SymbolColumnDelegate, LineColumnDelegate, ColorColumnDelegate, \
    AxisColumnDelegate
from correlationWindow import Ui_correlation
from mainWindow import Ui_Archiver
from pvs import Ui_Dialog
from baseplot import BasePlot, BasePlotCurveItem, TimeAxisItem
from baseplot_table_model import BasePlotCurvesModel
from datetime import datetime, timedelta
from epics import pv

intervals = [0, 0, 0, 0, 0, 0, 4, 8, 24, 48, 168, 336, 720, 4320, 6480, 8640]
plot_strategy = ['lastSample', 'firstSample', 'min', 'max', 'mean', 'median']
live_time = ['15m', '30m', '1h', '2h']


class ChildWindow(QDialog, Ui_Dialog):
    addSignal = pyqtSignal(str)

    def __init__(self):
        super(ChildWindow, self).__init__()
        self.setupUi(self)
        self._txtcur = self.textEdit.textCursor()
        self.textEdit.mouseDoubleClickEvent = self.mouseDoubleClickEvent

    def mouseDoubleClickEvent(self, event):
        txtcur = self.textEdit.textCursor()
        txtcur.movePosition(QTextCursor.EndOfLine)
        self.textEdit.setTextCursor(txtcur)
        txtcur.select(QTextCursor.LineUnderCursor)
        fmt = QTextCharFormat()
        fmt.setBackground(QBrush(QColor(0, 0, 255)))
        txtcur.mergeCharFormat(fmt)
        self.addSignal.emit(txtcur.selectedText())

    def addButton_click(self):
        txtcur = self.textEdit.textCursor()
        selected_text = []
        start = txtcur.selectionStart()
        end = txtcur.selectionEnd()
        if start == end:
            txtcur.movePosition(QTextCursor.StartOfLine, QTextCursor.KeepAnchor, 1)
            txtcur.select(QTextCursor.LineUnderCursor)
            selected_text.append(txtcur.selectedText())
        else:
            rows = txtcur.selectedText().splitlines().__len__()
            # print(txtcur.selectedText().splitlines())
            txtcur.setPosition(start, QTextCursor.MoveAnchor)
            txtcur.movePosition(QTextCursor.StartOfLine, QTextCursor.KeepAnchor, 1)
            for i in range(rows):
                txtcur.select(QTextCursor.LineUnderCursor)
                selected_text.append(txtcur.selectedText())
                txtcur.movePosition(QTextCursor.Down, QTextCursor.KeepAnchor, 1)
            # self.textEdit.setTextCursor(txtcur)
            # params = txtcur.selectedText().strip().replace(' ', '').replace('\n', '').replace('\r', '')
        self.addSignal.emit("\n".join(selected_text))


class CorrelationWindow(QDialog, Ui_correlation):

    def __init__(self):
        super(CorrelationWindow, self).__init__()
        self.setupUi(self)


class ParentWindow(QMainWindow, Ui_Archiver):
    plotSignal = pyqtSignal(BasePlot)

    def __init__(self):
        super(ParentWindow, self).__init__()
        self.setupUi(self)
        self.dateTimeEdit_start.setDateTime(QDateTime.currentDateTime().addSecs(-3600))
        self.dateTimeEdit_end.setDateTime(QDateTime.currentDateTime())
        # self.dateTimeEdit_start.lineEdit().setText("-1d")
        self.dateTimeEdit_start.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.dateTimeEdit_end.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.dateTimeEdit_start.setCalendarPopup(True)
        self.dateTimeEdit_end.setCalendarPopup(True)
        self.start_time = ''
        self.end_time = ''

        self.progressBar.setVisible(False)
        self.textEdit.setVisible(False)

        self.strategy_comboBox.addItems(plot_strategy)
        self.live_comboBox.addItems(live_time)
        self.x_axis_comboBox.addItem('Choose X Axis')

        # self.textEdit.setReadOnly(True)
        self._left_axis = AxisItem("left")
        # self._bottom_axis = TimeAxisItem('bottom')
        self._bottom_axis = DateAxisItem('bottom')
        # self.plotWidget = BasePlot(background='w', axisItems=None)
        self.plotWidget = BasePlot(background='w', axisItems={"bottom": self._bottom_axis, "left": self._left_axis})

        self.plotWidget.setShowXGrid(True)
        self.plotWidget.setShowYGrid(True)
        self.plotWidget.setShowLegend(True)
        self.plotWidget.enableCrosshair(is_enabled=True, vertical_movable=True, horizontal_movable=True)  # crosshair

        self.verticalLayout.addWidget(self.plotWidget)

        self.basePlotCurveEditor = BasePlotCurveEditor(plot=self.plotWidget, curves_tableView=self.curves_tableView,
                                                       axis_tableView=self.axis_tableView)
        #  self.basePlotCurveEditor = BasePlotCurveEditor(plot=self.plotWidget, curves_tableView=self.curves_tableView,
        #                                                axis_tableView=self.axis_tableView)

        self.add_axis_count = 0
        # self.basePlotCurveEditor.addAxisSignal.connect(self.fillAxisData)
        self.basePlotCurveEditor.curves_tableView.model().dataChanged.connect(self.fillAxisData)

        # self.tabWidget.currentChanged.connect(self.fillAxisData)
        # self.curves_model = BasePlotCurvesModel(None)
        # self.curves_tableView.setModel(self.curves_model)
        # self.axis_model = BasePlotAxesModel(None)
        # self.axis_tableView.setModel(self.axis_model)
        # self.setup_delegate_columns()
        self.timeButtonGroup.buttonClicked.connect(self.selectTime)
        self.plotSignal.connect(self.getPVs)

    def addButton_click(self):

        self.curves_tableView.model().append()

        record_name = self.lineEdit.text()
        if record_name != '':
            self.textEdit.append(record_name)

    def clearButton_click(self):
        self.textEdit.clear()

    def addFromChild_slot(self, params):
        for i in range(str(params).splitlines().__len__()):
            pv = str(params).split()[i]
            if pv != '':
                if not self.textEdit.find(pv, QTextDocument.FindCaseSensitively):
                    self.textEdit.append(pv)
                    self.curves_tableView.model().append(pvName=pv)
                    self.fillAxisData()
            self.textEdit.moveCursor(QTextCursor.Start)

    def searchButton_click(self):
        self._child = ChildWindow()
        # self._child.textEdit.copyAvailable['bool'].connect(self.on_textEdit_copyAvailable)
        pv = self.lineEdit.text().strip()
        if pv != '':
            url_string = os.environ.get('ARCHIVER_URL').__str__() + f":17665/mgmt/bpl/getAllPVs?pv=*{pv}*"
            print(os.environ.get('ARCHIVER_URL').__str__())
            req = urllib.request.urlopen(url_string)
            data = json.load(req)
            # print(data)
            for i in data:
                self._child.textEdit.append(i)
            self._child.addSignal.connect(self.addFromChild_slot)
            self._child.textEdit.setReadOnly(True)
            self._child.show()

    def addCurve(self):

        self.curves_tableView.model().append()
        record_name = self.lineEdit.text()
        if record_name != '':
            self.textEdit.append(record_name)
        self.fillAxisData()

    def removeSelectedCurve(self):
        pv = self.curves_tableView.currentIndex().data()
        if self.curves_tableView.currentIndex().row() >= 0:
            self.curves_tableView.model().removeAtIndex(self.curves_tableView.currentIndex())

        txtcur = self.textEdit.textCursor()
        while not txtcur.atEnd():
            txtcur.select(txtcur.LineUnderCursor)
            if txtcur.selectedText() == str(pv):
                txtcur.removeSelectedText()
                break
            txtcur.movePosition(QTextCursor.Down, QTextCursor.MoveAnchor)

        '''
        if self.textEdit.find(pv, QTextDocument.FindCaseSensitively):
            txtcur = self.textEdit.textCursor()
            txtcur.select(txtcur.BlockUnderCursor)
            txtcur.removeSelectedText()
        '''
        # print(self.textEdit.toPlainText())

    def clearCurve(self):
        self.textEdit.clear()
        self.curves_tableView.model().clear()

    def addAxis(self):
        self.add_axis_count += 1
        default_axis_name = 'New Axis ' + str(self.add_axis_count)
        # Just a quick way to ensure that the default named axes are always unique, even when the user closes
        # out a plot widget and re-opens it later
        # while default_axis_name in self.plot.plotItem.axes:
        while default_axis_name in self.plotWidget.plotItem.axes:
            self.add_axis_count += 1
            default_axis_name = 'New Axis ' + str(self.add_axis_count)
        self.axis_tableView.model().append(default_axis_name)

    def removeSelectedAxis(self):
        if self.axis_tableView.currentIndex().row() >= 0:
            self.axis_tableView.model().removeAtIndex(self.axis_tableView.currentIndex())

    def fillAxisData(self):
        if 'left' in self.plotWidget.plotItem.axes:
            self.plotWidget.plotItem.hideAxis('left')

        # self.plotWidget.plotItem.showAxis("left")
        axis_name_col_index = self.curves_tableView.model().getColumnIndex('Y-Axis Name')
        curve_axis_names = [str(self.curves_tableView.model().index(i, axis_name_col_index).data())
                            for i in range(self.curves_tableView.model().rowCount())]
        # print(curve_axis_names)
        existing_axis_names = [str(self.axis_tableView.model().index(i, 0).data())
                               for i in range(self.axis_tableView.model().rowCount())]
        # print(existing_axis_names)
        # Removing duplicates here instead of using a set to preserve order
        names_to_add = []
        for name in curve_axis_names:
            if name not in existing_axis_names and name not in names_to_add:
                names_to_add.append(name)
        # print(names_to_add)
        for name in names_to_add:
            if name:
                self.axis_tableView.model().append(name)
        self.axis_tableView.model().beginResetModel()
        time.sleep(0.1)
        self.axis_tableView.model().endResetModel()

    def saveChanges(self):
        self.plotWidget.setYAxes(self.plotWidget.yAxes)
        self.plotWidget.setCurves(self.plotWidget.curves)

    def plotButton_click(self):
        self.plotWidget.redraw_timer.stop()
        self.curves_tableView.clearSelection()
        self.axis_tableView.clearSelection()
        time.sleep(0.1)
        self.plotWidget.setYAxes(self.plotWidget.yAxes)
        self.plotWidget.setCurves(self.plotWidget.curves)

        start_time = self.dateTimeEdit_start.dateTime().toUTC()
        end_time = self.dateTimeEdit_end.dateTime().toUTC()
        timeformat = "yyyy-MM-ddThh:mm:ss"
        str_start_time = start_time.toString(timeformat) + 'Z'
        str_end_time = end_time.toString(timeformat) + 'Z'
        self.start_time = str_start_time
        self.end_time = str_end_time
        strategy = self.strategy_comboBox.currentText()
        if strategy == '':
            strategy = 'lastSample'

        self.progressBar.setVisible(True)
        self.progressBar.setFormat("Loading...")
        self.progressBar.setValue(10)
        for curve in self.plotWidget._curves:
            curve.setArchiverData(str_start_time, str_end_time, strategy)
            # self.plotWidget.plotItem.linkDataToAxis(plotDataItem=curve, axisName=curve.y_axis_name)
        self.plotWidget.plotItem.updateGrid()

        # self.resize(self.size() + QSize(0, random.choice((-1,1))))
        self.resize(self.size() + QSize(1, 0))
        self.resize(self.size() + QSize(-1, 0))
        '''
        self.verticalLayout.update()
        self.plotWidget.update()
        self.centralwidget.update()
        self.update()
        '''
        self.progressBar.setValue(100)
        self.progressBar.setFormat("Done")
        self.plotWidget.addItem(self.plotWidget.cursorlabel)
        self.plotSignal.emit(self.plotWidget)
        # pv = self.textEdit.toPlainText()
        # print(str_start_time)
        # curve = BasePlotCurveItem(color=None, lineStyle=None, lineWidth=None, yAxisName=None)
        # curve.setArchiverData(str_start_time, str_end_time, pv)
        # self.plotWdiget.addCurve(curve, curve_color='white', y_axis_name=None)
        # self.plotWidget.setBackgroundColor(QColor(255, 255, 255))
        # self.verticalLayout.addWidget(self.plotWdiget)

    def selectTime(self):
        self.plotWidget.redraw_timer.stop()
        self.curves_tableView.clearSelection()
        self.axis_tableView.clearSelection()
        text = self.timeButtonGroup.checkedButton().text()
        num_pattern = r"\d+"
        num = 0
        if re.findall(num_pattern, text).__len__() != 0:
            num = int(re.findall(num_pattern, text)[0])
        unit = re.sub(num_pattern, '', text)
        self.plotWidget.setYAxes(self.plotWidget.yAxes)
        self.plotWidget.setCurves(self.plotWidget.curves)

        time.sleep(0.1)

        start_time = datetime.utcnow()
        end_time = datetime.utcnow()
        if unit == "s":
            start_time = end_time - timedelta(seconds=num)
        elif unit == "m":
            start_time = end_time - timedelta(minutes=num)
        elif unit == "h":
            start_time = end_time - timedelta(hours=num)
        elif unit == "d":
            start_time = end_time - timedelta(days=num)
        elif unit == "w":
            start_time = end_time - timedelta(weeks=num)
        elif unit == "M":
            start_time = end_time - timedelta(days=num * 30)
        elif unit == "Y":
            start_time = end_time - timedelta(days=num * 30 * 12)
        elif unit == "YTD":
            current_year = datetime.today().year
            start_time = datetime.utcnow().replace(year=current_year, month=1, day=1, hour=0, minute=0, second=0,
                                                   microsecond=0)
        str_start_time = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        str_end_time = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")

        self.start_time = str_start_time
        self.end_time = str_end_time
        strategy = self.strategy_comboBox.currentText()
        if strategy == '':
            strategy = 'lastSample'
        timeformat = "yyyy-MM-ddThh:mm:ss"
        # str_start_time = start_time.toString(timeformat) + 'Z'
        # str_end_time = end_time.toString(timeformat) + 'Z'
        self.progressBar.setVisible(True)
        self.progressBar.setFormat("Loading...")
        self.progressBar.setValue(10)

        for curve in self.plotWidget._curves:
            curve.setArchiverData(str_start_time, str_end_time, strategy)
            # self.plotWidget.plotItem.linkDataToAxis(plotDataItem=curve, axisName=curve.y_axis_name)
            # In linkDataToAxis method, the curve is added again, so delete it.
            # self.plotWidget.plotItem.curves.remove(curve)

        self.plotWidget.plotItem.updateGrid()
        # self.resize(self.size() + QSize(0, random.choice((-1,1))))
        self.resize(self.size() + QSize(1, 0))
        self.resize(self.size() + QSize(-1, 0))
        self.plotSignal.emit(self.plotWidget)

        '''
        self.verticalLayout.update()
        self.plotWidget.update()
        self.centralwidget.update()
        self.update()
        '''

        self.progressBar.setValue(100)
        self.progressBar.setFormat("Done")
        self.plotWidget.addItem(self.plotWidget.cursorlabel)

    def chooseStrategy(self):
        self.curves_tableView.clearSelection()
        self.axis_tableView.clearSelection()
        time.sleep(0.1)
        self.plotWidget.setYAxes(self.plotWidget.yAxes)
        self.plotWidget.setCurves(self.plotWidget.curves)
        self.progressBar.setVisible(True)
        self.progressBar.setFormat("Loading...")
        self.progressBar.setValue(10)

        for curve in self.plotWidget._curves:
            curve.setArchiverData(self.start_time, self.end_time, strategy=self.strategy_comboBox.currentText())
            # self.plotWidget.plotItem.addLine(y=i, pen='r')
            # self.plotWidget.plotItem.linkDataToAxis(plotDataItem=curve, axisName=curve.y_axis_name)

        self.plotWidget.plotItem.updateGrid()
        self.resize(self.size() + QSize(1, 0))
        self.resize(self.size() + QSize(-1, 0))
        '''
        self.verticalLayout.update()
        self.plotWidget.update()
        self.centralwidget.update()
        self.update()
        '''
        self.progressBar.setValue(100)
        self.progressBar.setFormat("Done")
        self.plotWidget.addItem(self.plotWidget.cursorlabel)

    def getPVs(self, plotwidget):
        self.x_axis_comboBox.clear()
        self.x_axis_comboBox.addItem('Choose X Axis')
        curves_num = len(plotwidget._curves)
        if curves_num <= 1:
            return
        else:
            for curve in plotwidget._curves:
                self.x_axis_comboBox.addItem(curve.pv_name)
            self.x_axis_comboBox.activated['QString'].connect(lambda: self.correlatorPlot())
            # print(curve.xData)

    def correlatorPlot(self):
        '''
        class Ui_Dialog(object):
        class Ui_correlation(QtWidgets.QMainWindow):
        '''
        text = self.x_axis_comboBox.currentText()
        if text == 'Choose X Axis':
            return
        else:
            xdata = []
            self._correlationWin = CorrelationWindow()
            graph = pyqtgraph.GraphicsLayoutWidget()
            graph.setBackground('white')
            xCurve = None
            for curve in self.plotWidget._curves:
                if curve.pv_name == text:
                    (secs, vals) = curve.getCorrelatorData(start_time=self.start_time, end_time=self.end_time)
                    # print(secs)
                    xdata = vals
                    xCurve = curve

            for curve in self.plotWidget._curves:
                if curve.pv_name != text:
                    (secs, vals) = curve.getCorrelatorData(start_time=self.start_time, end_time=self.end_time)
                    ydata = vals
                    # print(secs)
                    if len(ydata) == len(xdata):
                        plot_item = graph.addPlot()
                        plot_item.setLabel(axis='bottom', text=f'<html style="color:{xCurve.color_string};'
                                                               f'font-size:12px;">{text}</html>')
                        plot_item.setLabel(axis='left', text=f'<html style="color:{curve.color_string};'
                                                             f'font-size:12px;">{curve.pv_name}</html>')
                        plot_item.showGrid(x=True, y=True)
                        # curve.color_strin
                        plot_data_item = plot_item.plot(xdata, ydata, pen=None, symbol='o', symbolSize=5,
                                                        symbolPen=curve.color_string)
                    graph.nextRow()
            self._correlationWin.verticalLayout.addWidget(graph)
            self._correlationWin.show()

    def chooseLiveTime(self):

        text = self.live_comboBox.currentText()

        num_pattern = r"\d+"
        num = 0
        if re.findall(num_pattern, text).__len__() != 0:
            num = int(re.findall(num_pattern, text)[0])
        unit = re.sub(num_pattern, '', text)
        start_time = datetime.utcnow()
        end_time = datetime.utcnow()
        if unit == "m":
            start_time = end_time - timedelta(minutes=num)
        elif unit == "h":
            start_time = end_time - timedelta(hours=num)

        str_start_time = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        str_end_time = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")

        self.start_time = str_start_time
        self.end_time = str_end_time

        self.curves_tableView.clearSelection()
        self.axis_tableView.clearSelection()
        time.sleep(0.1)
        self.plotWidget.setYAxes(self.plotWidget.yAxes)
        self.plotWidget.setCurves(self.plotWidget.curves)
        self.plotWidget.addItem(self.plotWidget.cursorlabel)
        # print(self.start_time)
        for curve in self.plotWidget._curves:
            (secs, vals) = curve.getArchiverData(self.start_time, self.end_time)
            curve.data_buffer = numpy.resize(curve.data_buffer, (2, len(secs)))
            curve.data_buffer[0] = secs
            curve.data_buffer[1] = vals
            curve.setData(x=secs, y=vals, stepMode="right", connect="all")
            # curve.data_buffer[0][:] = secs
            # curve.data_buffer[1][:] = vals
        self.plotWidget.plotItem.updateGrid()
        self.resize(self.size() + QSize(1, 0))
        self.resize(self.size() + QSize(-1, 0))
        # self.plotWidget.addItem(self.plotWidget.cursorlabel)
        self.plotWidget.redraw_timer.start()

    def exportData(self):
        timeformat = "%Y-%m-%dT%H:%M:%SZ"
        start_time = datetime.strptime(self.start_time, timeformat)
        end_time = datetime.strptime(self.end_time, timeformat)
        duration = end_time - start_time
        days = duration.days
        if days > 14:
            reply = QMessageBox.about(self, "Reminder", "The time interval cannot exceed 2 weeks.")
        else:
            filePath = QFileDialog.getSaveFileName(self, caption='Save File',
                                                   directory=os.path.expanduser('~') + '/Downloads',
                                                   filter='*.xls;;*.xlsx')

            if str(filePath[0]) != "":
                if str(filePath[1]) == "*.xls" or str(filePath[1]) == "*.xlsx":
                    fileName = filePath[0] + '.xls'
                    writer = pd.ExcelWriter(fileName, engine='openpyxl')
                    self.progressBar.setFormat("Loading...")
                    self.progressBar.setValue(10)


                    curve_num = 0
                    for curve in self.plotWidget._curves:

                        dict = {}
                        curve_num = curve_num + 1

                        pv_name = curve.pv_name
                        # print(pv_name)
                        url_string = os.environ.get(
                            'ARCHIVER_URL').__str__() + f":17668/retrieval/data/getData.json?pv={pv_name}&from={self.start_time}&to={self.end_time}&fetchLatestMetadata=true "
                        req = urllib.request.urlopen(url_string)
                        data = json.load(req)
                        secs = [x['secs'] for x in data[0]['data']]
                        vals = [x['val'] for x in data[0]['data']]
                        nanos = [x['nanos'] for x in data[0]['data']]
                        vals = vals[1:]
                        float_nanos = (numpy.array(nanos) * (1e-6))[1:]
                        secs = secs[1:] + float_nanos * (1e-3)
                        time_str_list = []
                        utc_time_list = []
                        i = 0
                        while i < secs.__len__():
                            utc_time_list.append(datetime(1970, 1, 1) + timedelta(seconds=secs[i]))
                            # time_obj=datetime(1970, 1, 1) + timedelta(seconds=secs[i])
                            time_obj = datetime.fromtimestamp(secs[i])
                            time_str = time_obj.strftime("%Y-%m-%d %H:%M:%S")
                            milliseconds = time_obj.microsecond // 1000
                            time_str_with_milliseconds = f"{time_str}.{milliseconds:03d}"
                            time_str_list.append(time_str_with_milliseconds)
                            i = i + 1
                        dict['Time'] = time_str_list
                        dict[pv_name] = vals
                        df1 = pd.DataFrame(dict)
                        df1.to_excel(writer, sheet_name=str(curve_num))

                    # dataframe = pd.DataFrame(dict)
                    # dataframe.to_csv(fileName, sep=',')
                    writer.close()
                    self.progressBar.setValue(100)
                    self.progressBar.setFormat("Done")
                    # self.setWindowModality(QtCore.Qt.NonModal)
                    # self.loadWin.close()

    def exportPlotData(self):
        # str_start_time = self.start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        # str_end_time = self.end_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        strategy = self.strategy_comboBox.currentText()
        if strategy == '':
            strategy = 'lastSample'
        filePath = QFileDialog.getSaveFileName(self, caption='Save File',
                                               directory=os.path.expanduser('~') + '/Downloads',
                                               filter='*.xls;;*.xlsx')

        if str(filePath[0]) != "":
            if str(filePath[1]) == "*.xls" or str(filePath[1]) == "*.xlsx":
                fileName = filePath[0] + '.xls'
                writer = pd.ExcelWriter(fileName, engine='openpyxl')
                self.progressBar.setFormat("Loading...")
                self.progressBar.setValue(10)

                curve_num = 0
                for curve in self.plotWidget._curves:
                    dict = {}
                    curve_num = curve_num + 1
                    pv_name = curve.pv_name
                    (secs, vals) = curve.getArchiverData(self.start_time, self.end_time, strategy)
                    time_str_list = []
                    utc_time_list = []
                    i = 0
                    while i < secs.__len__():
                        utc_time_list.append(datetime(1970, 1, 1) + timedelta(seconds=secs[i]))
                        # time_obj=datetime(1970, 1, 1) + timedelta(seconds=secs[i])
                        time_obj = datetime.fromtimestamp(secs[i])
                        time_str = time_obj.strftime("%Y-%m-%d %H:%M:%S")
                        milliseconds = time_obj.microsecond // 1000
                        time_str_with_milliseconds = f"{time_str}.{milliseconds:03d}"
                        time_str_list.append(time_str_with_milliseconds)
                        i = i + 1
                    dict['Time'] = time_str_list
                    dict[pv_name] = vals
                    df1 = pd.DataFrame(dict)
                    df1.to_excel(writer, sheet_name=str(curve_num))

                writer.close()
                self.progressBar.setValue(100)
                self.progressBar.setFormat("Done")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ParentWindow()
    window.show()

    sys.exit(app.exec())
    # url_string = "http://10.30.1.130:17665/mgmt/bpl/getAllPVs?pv=LINAC*"
    # req = urllib.request.urlopen(url_string)
    # data = json.load(req)
    # print(data)
