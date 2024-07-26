
from PyQt5.QtCore import pyqtSignal
from qtpy.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTableView,
                            QAbstractItemView, QSpacerItem, QSizePolicy,
                            QDialogButtonBox, QPushButton, QStyleOptionViewItem, QTabWidget, QWidget,
                            QComboBox, QStyledItemDelegate, QColorDialog, QHeaderView)
from qtpy.QtCore import Qt, Slot, QAbstractItemModel, QModelIndex, QObject, QItemSelection
from baseplot import BasePlotAxisItem, BasePlotCurveItem
from baseplot_table_model import BasePlotCurvesModel
from axis_table_model import BasePlotAxesModel
from collections import OrderedDict
from typing import Optional


class BasePlotCurveEditor(QWidget):
    """It is used to edit the properties of the curves.
    This thing is mostly just a wrapper for a table view, with a couple
    buttons to add and remove curves, and a button to save the changes."""
    TABLE_MODEL_CLASS = BasePlotCurvesModel
    AXIS_MODEL_CLASS = BasePlotAxesModel
    AXIS_MODEL_TAB_INDEX = 1
    addAxisSignal = pyqtSignal()

    def __init__(self, plot, curves_tableView, axis_tableView, parent=None):
        super(BasePlotCurveEditor, self).__init__(parent)

        self.plot = plot
        self.curves_tableView = curves_tableView
        self.axis_tableView = axis_tableView
        self.setup_ui()
        self.table_model = self.TABLE_MODEL_CLASS(self.plot)
        self.curves_tableView.setModel(self.table_model)
        self.curves_tableView.setColumnWidth(0, 200)
        self.curves_tableView.setColumnWidth(2, 50)

        self.table_model.plot = plot
        self.axis_model = self.AXIS_MODEL_CLASS(self.plot)
        self.axis_tableView.setModel(self.axis_model)
        self.axis_tableView.setColumnWidth(3, 150)
        self.axis_tableView.setColumnWidth(4, 150)
        self.axis_model.plot = plot
        self.setup_delegate_columns()

        # self.table_view.resizeColumnsToContents()
        '''
        self.add_button.clicked.connect(self.addCurve)
        self.remove_button.clicked.connect(self.removeSelectedCurve)
        self.add_axis_button.clicked.connect(self.addAxis)
        self.remove_axis_button.clicked.connect(self.removeSelectedAxis)
        self.remove_axis_button.setEnabled(False)
        self.add_axis_count = 0
        self.table_view.selectionModel().selectionChanged.connect(
            self.handleSelectionChange)
        self.axis_view.selectionModel().selectionChanged.connect(
            self.handleSelectionChange)
        '''
        self.curves_tableView.doubleClicked.connect(self.handleDoubleClick)
        #self.resize(800, 300)

    def setup_ui(self):
        self.curves_tableView.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.curves_tableView.setProperty("showDropIndicator", False)
        self.curves_tableView.setDragDropOverwriteMode(False)
        self.curves_tableView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.curves_tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.curves_tableView.setSortingEnabled(False)
        self.curves_tableView.horizontalHeader().setStretchLastSection(True)
        self.curves_tableView.verticalHeader().setVisible(False)
        self.curves_tableView.setColumnWidth(0, 160)
        self.curves_tableView.setColumnWidth(1, 160)
        self.curves_tableView.setColumnWidth(2, 160)

        self.axis_tableView.setDragDropOverwriteMode(False)
        self.axis_tableView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.axis_tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.axis_tableView.setSortingEnabled(False)
        #self.axis_tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.axis_tableView.verticalHeader().setVisible(False)

        #self.tab_widget.currentChanged.connect(self.fillAxisData)

        self.button_box = QDialogButtonBox(self)
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.addButton("Done", QDialogButtonBox.AcceptRole)

        #self.button_box.accepted.connect(self.saveChanges)
        #self.button_box.rejected.connect(self.reject)
        self.setWindowTitle("Waveform Curve Editor")

    def setup_delegate_columns(self):
        symbol_delegate = SymbolColumnDelegate(self)
        self.curves_tableView.setItemDelegateForColumn(self.table_model.getColumnIndex('Symbol'), symbol_delegate)
        line_delegate = LineColumnDelegate(self)
        self.curves_tableView.setItemDelegateForColumn(self.table_model.getColumnIndex('Line Style'), line_delegate)
        color_delegate = ColorColumnDelegate(self)
        self.curves_tableView.setItemDelegateForColumn(self.table_model.getColumnIndex('Color'), color_delegate)
        axis_delegate = AxisColumnDelegate(self)
        self.axis_tableView.setItemDelegateForColumn(self.axis_model.getColumnIndex('Y-Axis Orientation'), axis_delegate)

    @Slot(QModelIndex)
    def handleDoubleClick(self, index):
        if self.curves_tableView.model().needsColorDialog(index):
        #if self.table_model.needsColorDialog(index):
            # The table model returns a QBrush for BackgroundRole, not a QColor
            init_color = self.curves_tableView.model().data(index,
                                               Qt.BackgroundRole).color()
            color = QColorDialog.getColor(init_color, self)
            if color.isValid():
                self.curves_tableView.model().setData(index, color, role=Qt.EditRole)
        #elif self.curves_tableView.model().needsAddAxis(index):
        #    self.addAxisSignal.emit()

class ColorColumnDelegate(QStyledItemDelegate):
    """The ColorColumnDelegate is an item delegate that is installed on the
    color column of the table view.  Its only job is to ensure that the default
    editor widget (a line edit) isn't displayed for items in the color column.
    """
    def createEditor(self, parent, option, index):
        return None


class AxisColumnDelegate(QStyledItemDelegate):

    """
    AxisColumnDelegate draws a QComboBox with the allowed values for the axis orientation
    column value, which must map to the values expected by PyQtGraph. Helps ensure that the
    user doesn't have to know what these exact values are, and prevents frustrating typos.
    """
    def createEditor(self, parent, option, index):
        editor = QComboBox(parent)
        editor.addItems(BasePlotAxisItem.axis_orientations.keys())
        return editor

    def setEditorData(self, editor, index):
        val = str(index.model().data(index, Qt.EditRole))
        editor.setCurrentText(val)

    def setModelData(self, editor, model, index):
        val = BasePlotAxisItem.axis_orientations[editor.currentText()]
        model.setData(index, val, Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class LineColumnDelegate(QStyledItemDelegate):
    """LineColumnDelegate draws a QComboBox in the Line Style column, so that users
    can pick the styles they want to display from a list, instead of needing to
    remember the PyQtGraph character codes."""
    def createEditor(self, parent, option, index):
        editor = QComboBox(parent)
        editor.addItems(BasePlotCurveItem.lines.keys())
        return editor

    def setEditorData(self, editor, index):
        val = str(index.model().data(index, Qt.EditRole))
        editor.setCurrentText(val)

    def setModelData(self, editor, model, index):
        val = BasePlotCurveItem.lines[editor.currentText()]
        model.setData(index, val, Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class SymbolColumnDelegate(QStyledItemDelegate):
    """SymbolColumnDelegate draws a QComboBox in the Symbol column, so that users
    can pick the symbol they want to display from a list, instead of needing to
    remember the PyQtGraph character codes."""
    def createEditor(self, parent, option, index):
        editor = QComboBox(parent)
        editor.addItems(BasePlotCurveItem.symbols.keys())
        return editor

    def setEditorData(self, editor, index):
        val = str(index.model().data(index, Qt.EditRole))
        editor.setCurrentText(val)

    def setModelData(self, editor, model, index):
        val = BasePlotCurveItem.symbols[editor.currentText()]
        model.setData(index, val, Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class RedrawModeColumnDelegate(QStyledItemDelegate):
    """RedrawModeColumnDelegate draws a QComboBox in the Redraw Mode column, so
    that users can pick the redraw mode from a list."""
    choices = OrderedDict([
        ('X or Y updates', BasePlotCurveItem.REDRAW_ON_EITHER),
        ('Y updates', BasePlotCurveItem.REDRAW_ON_Y),
        ('X updates', BasePlotCurveItem.REDRAW_ON_X),
        ('Both update', BasePlotCurveItem.REDRAW_ON_BOTH)])
    text_for_choices = {v: k for k, v in choices.items()}

    def displayText(self, value, locale):
        return self.text_for_choices[value]

    def createEditor(self, parent, option, index):
        editor = QComboBox(parent)
        editor.addItems(self.choices.keys())
        return editor

    def setEditorData(self, editor, index):
        val = self.text_for_choices[index.model().data(index, Qt.EditRole)]
        editor.setCurrentText(val)

    def setModelData(self, editor, model, index):
        val = self.choices[editor.currentText()]
        model.setData(index, val, Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class PlotStyleColumnDelegate(QStyledItemDelegate):
    """ Allows the user to toggle between line and bar graphs. Hides/shows relevant columns based on that choice. """

    line_columns_to_toggle = ('Line Style', 'Line Width', 'Symbol', 'Symbol Size')
    bar_columns_to_toggle = ('Bar Width', 'Upper Limit', 'Lower Limit', 'Limit Color')

    def __init__(self, parent: QObject, table_model: BasePlotCurvesModel, table_view: QTableView):
        super().__init__(parent)
        self.table_model = table_model
        self.table_view = table_view

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> QWidget:
        """ Create a combo box that allows the user to choose the style of plot they want. """
        editor = QComboBox(parent)
        editor.addItems(('Line', 'Bar'))
        return editor

    def setEditorData(self, editor: QWidget, index: QModelIndex) -> None:
        val = str(index.model().data(index, Qt.EditRole))
        editor.setCurrentText(val)

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex) -> None:
        model.setData(index, editor.currentText(), Qt.EditRole)
        self.toggleColumnVisibility()

    def updateEditorGeometry(self, editor: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        editor.setGeometry(option.rect)

    def toggleColumnVisibility(self):
        """ Toggle visibility of columns based on the current state of the associated curve editor table """
        self.hideColumns(hide_line_columns=True, hide_bar_columns=True)
        if len(self.table_model.plot._curves) > 0:
            for curve in self.table_model.plot._curves:
                plot_style = curve.plot_style
                if plot_style is None or plot_style == 'Line':
                    self.hideColumns(hide_line_columns=False)
                elif plot_style == 'Bar':
                    self.hideColumns(hide_bar_columns=False)
        else:
            self.hideColumns(False, True)  # Show line columns only as a default

    def hideColumns(self, hide_line_columns: Optional[bool] = None, hide_bar_columns: Optional[bool] = None) -> None:
        """ Show or hide columns related to a specific plot style based on the input. If an input parameter
            is omitted (or explicitly set to None), the associated columns will be left alone. """

        if hide_line_columns is not None:
            for column in self.line_columns_to_toggle:
                self.table_view.setColumnHidden(self.table_model.getColumnIndex(column), hide_line_columns)
        if hide_bar_columns is not None:
            for column in self.bar_columns_to_toggle:
                self.table_view.setColumnHidden(self.table_model.getColumnIndex(column), hide_bar_columns)
