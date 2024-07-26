# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ArchiverViewer.ui'
#
# Created by: PyQt5 UI code generator 5.12.3

# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(2100, 1500)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.dateTimeEdit = QtWidgets.QDateTimeEdit(Form)
        self.dateTimeEdit.setGeometry(QtCore.QRect(60, 130, 194, 27))
        self.dateTimeEdit.setObjectName("dateTimeEdit")
        self.dateTimeEdit_2 = QtWidgets.QDateTimeEdit(Form)
        self.dateTimeEdit_2.setGeometry(QtCore.QRect(310, 130, 194, 27))
        self.dateTimeEdit_2.setObjectName("dateTimeEdit_2")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 130, 41, 18))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(270, 130, 41, 18))
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(70, 180, 301, 26))
        self.lineEdit.setObjectName("lineEdit")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(10, 180, 51, 18))
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(70, 220, 80, 26))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(180, 220, 80, 26))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(290, 220, 80, 26))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(390, 180, 80, 26))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(Form)
        self.pushButton_5.setGeometry(QtCore.QRect(1370, 350, 80, 26))
        self.pushButton_5.setStyleSheet("background-color: rgb(0, 255, 0);")
        self.pushButton_5.setObjectName("pushButton_5")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(30, 380, 2041, 641))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setGeometry(QtCore.QRect(502, 130, 821, 221))
        self.tabWidget.setObjectName("tabWidget")
        self.curves_tab = QtWidgets.QWidget()
        self.curves_tab.setObjectName("curves_tab")
        self.curves_tableView = QtWidgets.QTableView(self.curves_tab)
        self.curves_tableView.setGeometry(QtCore.QRect(-1, 1, 821, 151))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.curves_tableView.sizePolicy().hasHeightForWidth())
        self.curves_tableView.setSizePolicy(sizePolicy)
        self.curves_tableView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.curves_tableView.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)
        self.curves_tableView.setProperty("showDropIndicator", False)
        self.curves_tableView.setDragDropOverwriteMode(False)
        self.curves_tableView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.curves_tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.curves_tableView.setObjectName("curves_tableView")
        self.curves_tableView.horizontalHeader().setCascadingSectionResizes(True)
        self.curves_tableView.horizontalHeader().setHighlightSections(False)
        self.curves_tableView.horizontalHeader().setStretchLastSection(True)
        self.curves_tableView.verticalHeader().setVisible(False)
        self.curves_tableView.verticalHeader().setHighlightSections(False)
        self.add_curve_button = QtWidgets.QPushButton(self.curves_tab)
        self.add_curve_button.setGeometry(QtCore.QRect(360, 160, 101, 26))
        self.add_curve_button.setObjectName("add_curve_button")
        self.remove_curve_button = QtWidgets.QPushButton(self.curves_tab)
        self.remove_curve_button.setGeometry(QtCore.QRect(480, 160, 101, 26))
        self.remove_curve_button.setObjectName("remove_curve_button")
        self.tabWidget.addTab(self.curves_tab, "")
        self.axis_tab = QtWidgets.QWidget()
        self.axis_tab.setObjectName("axis_tab")
        self.axis_tableView = QtWidgets.QTableView(self.axis_tab)
        self.axis_tableView.setGeometry(QtCore.QRect(-1, 1, 821, 151))
        self.axis_tableView.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)
        self.axis_tableView.setTabKeyNavigation(True)
        self.axis_tableView.setProperty("showDropIndicator", False)
        self.axis_tableView.setDragDropOverwriteMode(False)
        self.axis_tableView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.axis_tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.axis_tableView.setObjectName("axis_tableView")
        self.axis_tableView.horizontalHeader().setHighlightSections(False)
        self.axis_tableView.horizontalHeader().setStretchLastSection(True)
        self.axis_tableView.verticalHeader().setVisible(False)
        self.axis_tableView.verticalHeader().setHighlightSections(False)
        self.add_axis_button = QtWidgets.QPushButton(self.axis_tab)
        self.add_axis_button.setGeometry(QtCore.QRect(370, 160, 101, 26))
        self.add_axis_button.setObjectName("add_axis_button")
        self.remove_axis_button = QtWidgets.QPushButton(self.axis_tab)
        self.remove_axis_button.setGeometry(QtCore.QRect(490, 160, 101, 26))
        self.remove_axis_button.setObjectName("remove_axis_button")
        self.tabWidget.addTab(self.axis_tab, "")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(0, 0, 1920, 111))
        font = QtGui.QFont()
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_4.setStyleSheet("background-color: rgb(112, 200, 251);\n"
"color: rgb(255, 255, 255);")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.tabWidget_2 = QtWidgets.QTabWidget(Form)
        self.tabWidget_2.setGeometry(QtCore.QRect(1320, 130, 750, 221))
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.axis_tab_2 = QtWidgets.QWidget()
        self.axis_tab_2.setObjectName("axis_tab_2")
        self.axis_tableView_2 = QtWidgets.QTableView(self.axis_tab_2)
        self.axis_tableView_2.setGeometry(QtCore.QRect(0, 0, 751, 151))
        self.axis_tableView_2.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)
        self.axis_tableView_2.setTabKeyNavigation(True)
        self.axis_tableView_2.setProperty("showDropIndicator", False)
        self.axis_tableView_2.setDragDropOverwriteMode(False)
        self.axis_tableView_2.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.axis_tableView_2.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.axis_tableView_2.setObjectName("axis_tableView_2")
        self.axis_tableView_2.horizontalHeader().setHighlightSections(False)
        self.axis_tableView_2.horizontalHeader().setStretchLastSection(True)
        self.axis_tableView_2.verticalHeader().setVisible(False)
        self.axis_tableView_2.verticalHeader().setHighlightSections(False)
        self.add_axis_button_2 = QtWidgets.QPushButton(self.axis_tab_2)
        self.add_axis_button_2.setGeometry(QtCore.QRect(370, 160, 101, 26))
        self.add_axis_button_2.setObjectName("add_axis_button_2")
        self.remove_axis_button_2 = QtWidgets.QPushButton(self.axis_tab_2)
        self.remove_axis_button_2.setGeometry(QtCore.QRect(490, 160, 101, 26))
        self.remove_axis_button_2.setObjectName("remove_axis_button_2")
        self.tabWidget_2.addTab(self.axis_tab_2, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget_2.addTab(self.tab_2, "")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(70, 260, 391, 70))
        self.textEdit.setObjectName("textEdit")

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)
        self.pushButton.clicked.connect(Form.addButton_click)
        self.pushButton_2.clicked.connect(Form.deleteButton_click)
        self.pushButton_4.clicked.connect(Form.searchButton_click)
        self.pushButton_3.clicked.connect(Form.clearButton_click)
        self.pushButton_5.clicked.connect(Form.plotButton_click)
        self.add_axis_button.clicked.connect(Form.addAxis)
        self.remove_axis_button.clicked.connect(Form.removeSelectedAxis)
        self.tabWidget.currentChanged['int'].connect(Form.fillAxisData)
        self.add_curve_button.clicked.connect(Form.addCurve)
        self.remove_curve_button.clicked.connect(Form.removeSelectedCurve)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Start"))
        self.label_2.setText(_translate("Form", "End"))
        self.label_3.setText(_translate("Form", "Channel"))
        self.pushButton.setText(_translate("Form", "Add"))
        self.pushButton_2.setText(_translate("Form", "Remove"))
        self.pushButton_3.setText(_translate("Form", "Clear"))
        self.pushButton_4.setText(_translate("Form", "Search"))
        self.pushButton_5.setText(_translate("Form", "Plot"))
        self.add_curve_button.setText(_translate("Form", "Add Curve"))
        self.remove_curve_button.setText(_translate("Form", "Remove Curve"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.curves_tab), _translate("Form", "Tab 1"))
        self.add_axis_button.setText(_translate("Form", "Add Axis"))
        self.remove_axis_button.setText(_translate("Form", "Remove Axis"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.axis_tab), _translate("Form", "Tab 2"))
        self.label_4.setText(_translate("Form", "SHINE Accelerator Archiver System"))
        self.add_axis_button_2.setText(_translate("Form", "Add Axis"))
        self.remove_axis_button_2.setText(_translate("Form", "Remove Axis"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.axis_tab_2), _translate("Form", "Tab 1"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_2), _translate("Form", "Tab 2"))
