# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Archiver(object):
    def setupUi(self, Archiver):
        Archiver.setObjectName("Archiver")
        Archiver.resize(2000, 1000)
        Archiver.setStyleSheet("background-color: rgb(239, 239, 239);")
        self.centralwidget = QtWidgets.QWidget(Archiver)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(20, 10, 20, 30)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_4.setStyleSheet("background-color: rgb(112, 200, 251);\n"
"color: rgb(255, 255, 255);")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setMaximumSize(QtCore.QSize(1000, 16777215))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout.setObjectName("gridLayout")
        self.searchButton = QtWidgets.QPushButton(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchButton.sizePolicy().hasHeightForWidth())
        self.searchButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.searchButton.setFont(font)
        self.searchButton.setStyleSheet("background-color: rgb(0, 255, 0);")
        self.searchButton.setObjectName("searchButton")
        self.gridLayout.addWidget(self.searchButton, 1, 1, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.label_13.setFont(font)
        self.label_13.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_13.setObjectName("label_13")
        self.gridLayout.addWidget(self.label_13, 2, 0, 1, 1)
        self.dateTimeEdit_start = QtWidgets.QDateTimeEdit(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dateTimeEdit_start.sizePolicy().hasHeightForWidth())
        self.dateTimeEdit_start.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.dateTimeEdit_start.setFont(font)
        self.dateTimeEdit_start.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.dateTimeEdit_start.setObjectName("dateTimeEdit_start")
        self.gridLayout.addWidget(self.dateTimeEdit_start, 2, 1, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.label_14.setFont(font)
        self.label_14.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_14.setObjectName("label_14")
        self.gridLayout.addWidget(self.label_14, 3, 0, 1, 1)
        self.dateTimeEdit_end = QtWidgets.QDateTimeEdit(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dateTimeEdit_end.sizePolicy().hasHeightForWidth())
        self.dateTimeEdit_end.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.dateTimeEdit_end.setFont(font)
        self.dateTimeEdit_end.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.dateTimeEdit_end.setObjectName("dateTimeEdit_end")
        self.gridLayout.addWidget(self.dateTimeEdit_end, 3, 1, 1, 1)
        self.plotButton = QtWidgets.QPushButton(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plotButton.sizePolicy().hasHeightForWidth())
        self.plotButton.setSizePolicy(sizePolicy)
        self.plotButton.setStyleSheet("background-color: rgb(0, 255, 0);")
        self.plotButton.setObjectName("plotButton")
        self.gridLayout.addWidget(self.plotButton, 4, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.label_11.setFont(font)
        self.label_11.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 0, 0, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.progressBar.setFont(font)
        self.progressBar.setMaximum(100)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(True)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 5, 1, 1, 1)
        self.horizontalLayout.addWidget(self.frame_2)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setContentsMargins(0, -1, 0, -1)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMaximumSize(QtCore.QSize(2000, 1000))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.curves_tableView = QtWidgets.QTableView(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.curves_tableView.sizePolicy().hasHeightForWidth())
        self.curves_tableView.setSizePolicy(sizePolicy)
        self.curves_tableView.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"selection-color: rgb(0, 0, 0);\n"
"selection-background-color: rgb(0, 170, 255);")
        self.curves_tableView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.curves_tableView.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)
        self.curves_tableView.setTabKeyNavigation(False)
        self.curves_tableView.setProperty("showDropIndicator", False)
        self.curves_tableView.setDragDropOverwriteMode(False)
        self.curves_tableView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.curves_tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.curves_tableView.setObjectName("curves_tableView")
        self.curves_tableView.horizontalHeader().setCascadingSectionResizes(True)
        self.curves_tableView.horizontalHeader().setHighlightSections(False)
        self.curves_tableView.horizontalHeader().setStretchLastSection(True)
        self.curves_tableView.verticalHeader().setVisible(False)
        self.curves_tableView.verticalHeader().setDefaultSectionSize(20)
        self.curves_tableView.verticalHeader().setHighlightSections(False)
        self.curves_tableView.verticalHeader().setMinimumSectionSize(20)
        self.verticalLayout_4.addWidget(self.curves_tableView)
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setStyleSheet("")
        self.frame_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setLineWidth(1)
        self.frame_4.setObjectName("frame_4")
        self.add_curve_button = QtWidgets.QPushButton(self.frame_4)
        self.add_curve_button.setGeometry(QtCore.QRect(10, 0, 80, 26))
        self.add_curve_button.setObjectName("add_curve_button")
        self.remove_curve_button = QtWidgets.QPushButton(self.frame_4)
        self.remove_curve_button.setGeometry(QtCore.QRect(100, 0, 89, 26))
        self.remove_curve_button.setObjectName("remove_curve_button")
        self.clear_curve_button = QtWidgets.QPushButton(self.frame_4)
        self.clear_curve_button.setGeometry(QtCore.QRect(200, 0, 80, 26))
        self.clear_curve_button.setObjectName("clear_curve_button")
        self.textEdit = QtWidgets.QTextEdit(self.frame_4)
        self.textEdit.setGeometry(QtCore.QRect(310, 0, 201, 41))
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout_4.addWidget(self.frame_4)
        self.verticalLayout_4.setStretch(0, 5)
        self.verticalLayout_4.setStretch(1, 1)
        self.horizontalLayout_2.addWidget(self.frame)
        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setMaximumSize(QtCore.QSize(2000, 1000))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.axis_tableView = QtWidgets.QTableView(self.frame_3)
        self.axis_tableView.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"selection-color: rgb(0, 0, 0);\n"
"selection-background-color: rgb(0, 170, 255);")
        self.axis_tableView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.axis_tableView.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)
        self.axis_tableView.setTabKeyNavigation(False)
        self.axis_tableView.setProperty("showDropIndicator", False)
        self.axis_tableView.setDragDropOverwriteMode(False)
        self.axis_tableView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.axis_tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.axis_tableView.setObjectName("axis_tableView")
        self.axis_tableView.horizontalHeader().setCascadingSectionResizes(True)
        self.axis_tableView.horizontalHeader().setHighlightSections(False)
        self.axis_tableView.horizontalHeader().setStretchLastSection(True)
        self.axis_tableView.verticalHeader().setVisible(False)
        self.axis_tableView.verticalHeader().setDefaultSectionSize(20)
        self.axis_tableView.verticalHeader().setHighlightSections(False)
        self.axis_tableView.verticalHeader().setMinimumSectionSize(20)
        self.verticalLayout_5.addWidget(self.axis_tableView)
        self.frame_5 = QtWidgets.QFrame(self.frame_3)
        self.frame_5.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.remove_axis_button = QtWidgets.QPushButton(self.frame_5)
        self.remove_axis_button.setGeometry(QtCore.QRect(100, 0, 80, 26))
        self.remove_axis_button.setObjectName("remove_axis_button")
        self.add_axis_button = QtWidgets.QPushButton(self.frame_5)
        self.add_axis_button.setGeometry(QtCore.QRect(10, 0, 80, 26))
        self.add_axis_button.setObjectName("add_axis_button")
        self.add_axis_button.raise_()
        self.remove_axis_button.raise_()
        self.verticalLayout_5.addWidget(self.frame_5)
        self.verticalLayout_5.setStretch(0, 5)
        self.verticalLayout_5.setStretch(1, 1)
        self.horizontalLayout_2.addWidget(self.frame_3)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 1)
        self.verticalLayout_6.addLayout(self.horizontalLayout_2)
        self.frame1 = QtWidgets.QFrame(self.centralwidget)
        self.frame1.setMaximumSize(QtCore.QSize(3000, 200))
        self.frame1.setStyleSheet("")
        self.frame1.setObjectName("frame1")
        self.pushButton1 = QtWidgets.QPushButton(self.frame1)
        self.pushButton1.setGeometry(QtCore.QRect(1, 15, 50, 26))
        self.pushButton1.setCheckable(True)
        self.pushButton1.setAutoExclusive(True)
        self.pushButton1.setObjectName("pushButton1")
        self.timeButtonGroup = QtWidgets.QButtonGroup(Archiver)
        self.timeButtonGroup.setObjectName("timeButtonGroup")
        self.timeButtonGroup.addButton(self.pushButton1)
        self.pushButton2 = QtWidgets.QPushButton(self.frame1)
        self.pushButton2.setGeometry(QtCore.QRect(60, 15, 50, 26))
        self.pushButton2.setCheckable(True)
        self.pushButton2.setAutoExclusive(True)
        self.pushButton2.setObjectName("pushButton2")
        self.timeButtonGroup.addButton(self.pushButton2)
        self.pushButton4 = QtWidgets.QPushButton(self.frame1)
        self.pushButton4.setGeometry(QtCore.QRect(180, 15, 50, 26))
        self.pushButton4.setCheckable(True)
        self.pushButton4.setAutoExclusive(True)
        self.pushButton4.setObjectName("pushButton4")
        self.timeButtonGroup.addButton(self.pushButton4)
        self.pushButton3 = QtWidgets.QPushButton(self.frame1)
        self.pushButton3.setGeometry(QtCore.QRect(120, 15, 50, 26))
        self.pushButton3.setCheckable(True)
        self.pushButton3.setAutoExclusive(True)
        self.pushButton3.setObjectName("pushButton3")
        self.timeButtonGroup.addButton(self.pushButton3)
        self.pushButton8 = QtWidgets.QPushButton(self.frame1)
        self.pushButton8.setGeometry(QtCore.QRect(420, 15, 50, 26))
        self.pushButton8.setCheckable(True)
        self.pushButton8.setAutoExclusive(True)
        self.pushButton8.setObjectName("pushButton8")
        self.timeButtonGroup.addButton(self.pushButton8)
        self.pushButton6 = QtWidgets.QPushButton(self.frame1)
        self.pushButton6.setGeometry(QtCore.QRect(300, 15, 50, 26))
        self.pushButton6.setCheckable(True)
        self.pushButton6.setChecked(False)
        self.pushButton6.setAutoExclusive(True)
        self.pushButton6.setObjectName("pushButton6")
        self.timeButtonGroup.addButton(self.pushButton6)
        self.pushButton7 = QtWidgets.QPushButton(self.frame1)
        self.pushButton7.setGeometry(QtCore.QRect(360, 15, 50, 26))
        self.pushButton7.setCheckable(True)
        self.pushButton7.setAutoExclusive(True)
        self.pushButton7.setObjectName("pushButton7")
        self.timeButtonGroup.addButton(self.pushButton7)
        self.pushButton5 = QtWidgets.QPushButton(self.frame1)
        self.pushButton5.setGeometry(QtCore.QRect(240, 15, 50, 26))
        self.pushButton5.setCheckable(True)
        self.pushButton5.setAutoExclusive(True)
        self.pushButton5.setObjectName("pushButton5")
        self.timeButtonGroup.addButton(self.pushButton5)
        self.pushButton12 = QtWidgets.QPushButton(self.frame1)
        self.pushButton12.setGeometry(QtCore.QRect(660, 15, 50, 26))
        self.pushButton12.setCheckable(True)
        self.pushButton12.setAutoExclusive(True)
        self.pushButton12.setObjectName("pushButton12")
        self.timeButtonGroup.addButton(self.pushButton12)
        self.pushButton15 = QtWidgets.QPushButton(self.frame1)
        self.pushButton15.setGeometry(QtCore.QRect(840, 15, 50, 26))
        self.pushButton15.setCheckable(True)
        self.pushButton15.setAutoExclusive(True)
        self.pushButton15.setObjectName("pushButton15")
        self.timeButtonGroup.addButton(self.pushButton15)
        self.pushButton10 = QtWidgets.QPushButton(self.frame1)
        self.pushButton10.setGeometry(QtCore.QRect(540, 15, 50, 26))
        self.pushButton10.setCheckable(True)
        self.pushButton10.setAutoExclusive(True)
        self.pushButton10.setObjectName("pushButton10")
        self.timeButtonGroup.addButton(self.pushButton10)
        self.pushButton14 = QtWidgets.QPushButton(self.frame1)
        self.pushButton14.setGeometry(QtCore.QRect(780, 15, 50, 26))
        self.pushButton14.setCheckable(True)
        self.pushButton14.setAutoExclusive(True)
        self.pushButton14.setObjectName("pushButton14")
        self.timeButtonGroup.addButton(self.pushButton14)
        self.pushButton11 = QtWidgets.QPushButton(self.frame1)
        self.pushButton11.setGeometry(QtCore.QRect(600, 15, 50, 26))
        self.pushButton11.setCheckable(True)
        self.pushButton11.setAutoExclusive(True)
        self.pushButton11.setObjectName("pushButton11")
        self.timeButtonGroup.addButton(self.pushButton11)
        self.pushButton16 = QtWidgets.QPushButton(self.frame1)
        self.pushButton16.setGeometry(QtCore.QRect(900, 15, 50, 26))
        self.pushButton16.setCheckable(True)
        self.pushButton16.setAutoExclusive(True)
        self.pushButton16.setObjectName("pushButton16")
        self.timeButtonGroup.addButton(self.pushButton16)
        self.pushButton13 = QtWidgets.QPushButton(self.frame1)
        self.pushButton13.setGeometry(QtCore.QRect(720, 15, 50, 26))
        self.pushButton13.setCheckable(True)
        self.pushButton13.setAutoExclusive(True)
        self.pushButton13.setObjectName("pushButton13")
        self.timeButtonGroup.addButton(self.pushButton13)
        self.pushButton9 = QtWidgets.QPushButton(self.frame1)
        self.pushButton9.setGeometry(QtCore.QRect(480, 15, 50, 26))
        self.pushButton9.setCheckable(True)
        self.pushButton9.setAutoExclusive(True)
        self.pushButton9.setObjectName("pushButton9")
        self.timeButtonGroup.addButton(self.pushButton9)
        self.strategy_comboBox = QtWidgets.QComboBox(self.frame1)
        self.strategy_comboBox.setGeometry(QtCore.QRect(1150, 15, 101, 26))
        self.strategy_comboBox.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"selection-color: rgb(0, 0, 0);\n"
"selection-background-color: rgb(0, 170, 255);")
        self.strategy_comboBox.setObjectName("strategy_comboBox")
        self.label = QtWidgets.QLabel(self.frame1)
        self.label.setGeometry(QtCore.QRect(1069, 20, 81, 18))
        self.label.setObjectName("label")
        self.export_pushButton = QtWidgets.QPushButton(self.frame1)
        self.export_pushButton.setGeometry(QtCore.QRect(1500, 15, 101, 26))
        self.export_pushButton.setStyleSheet("background-color: rgb(85, 170, 255);")
        self.export_pushButton.setIconSize(QtCore.QSize(25, 25))
        self.export_pushButton.setCheckable(False)
        self.export_pushButton.setAutoExclusive(False)
        self.export_pushButton.setObjectName("export_pushButton")
        self.export_plot_pushButton = QtWidgets.QPushButton(self.frame1)
        self.export_plot_pushButton.setGeometry(QtCore.QRect(1610, 15, 101, 26))
        self.export_plot_pushButton.setStyleSheet("background-color: rgb(85, 170, 255);")
        self.export_plot_pushButton.setIconSize(QtCore.QSize(25, 25))
        self.export_plot_pushButton.setCheckable(False)
        self.export_plot_pushButton.setAutoExclusive(False)
        self.export_plot_pushButton.setObjectName("export_plot_pushButton")
        self.label_2 = QtWidgets.QLabel(self.frame1)
        self.label_2.setGeometry(QtCore.QRect(959, 20, 41, 18))
        self.label_2.setObjectName("label_2")
        self.live_comboBox = QtWidgets.QComboBox(self.frame1)
        self.live_comboBox.setGeometry(QtCore.QRect(989, 15, 61, 26))
        self.live_comboBox.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"selection-color: rgb(0, 0, 0);\n"
"selection-background-color: rgb(0, 170, 255);")
        self.live_comboBox.setObjectName("live_comboBox")
        self.x_axis_comboBox = QtWidgets.QComboBox(self.frame1)
        self.x_axis_comboBox.setGeometry(QtCore.QRect(1340, 15, 141, 26))
        self.x_axis_comboBox.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"selection-color: rgb(0, 0, 0);\n"
"selection-background-color: rgb(0, 170, 255);")
        self.x_axis_comboBox.setObjectName("x_axis_comboBox")
        self.label_3 = QtWidgets.QLabel(self.frame1)
        self.label_3.setGeometry(QtCore.QRect(1270, 20, 71, 18))
        self.label_3.setObjectName("label_3")
        self.verticalLayout_6.addWidget(self.frame1)
        self.verticalLayout_6.setStretch(0, 4)
        self.verticalLayout_6.setStretch(1, 1)
        self.horizontalLayout.addLayout(self.verticalLayout_6)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 8)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 4)
        self.verticalLayout_2.setStretch(2, 8)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        Archiver.setCentralWidget(self.centralwidget)

        self.retranslateUi(Archiver)
        self.searchButton.clicked.connect(Archiver.searchButton_click)
        self.plotButton.clicked.connect(Archiver.plotButton_click)
        self.add_axis_button.clicked.connect(Archiver.addAxis)
        self.remove_axis_button.clicked.connect(Archiver.removeSelectedAxis)
        self.remove_curve_button.clicked.connect(Archiver.removeSelectedCurve)
        self.add_curve_button.clicked.connect(Archiver.addCurve)
        self.clear_curve_button.clicked.connect(Archiver.clearCurve)
        self.strategy_comboBox.activated['QString'].connect(Archiver.chooseStrategy)
        self.export_pushButton.clicked.connect(Archiver.exportData)
        self.export_plot_pushButton.clicked.connect(Archiver.exportPlotData)
        self.live_comboBox.activated['QString'].connect(Archiver.chooseLiveTime)
        QtCore.QMetaObject.connectSlotsByName(Archiver)

    def retranslateUi(self, Archiver):
        _translate = QtCore.QCoreApplication.translate
        Archiver.setWindowTitle(_translate("Archiver", "Archiver"))
        self.label_4.setText(_translate("Archiver", "SHINE Accelerator Archiver System"))
        self.searchButton.setText(_translate("Archiver", "Search"))
        self.label_13.setText(_translate("Archiver", "Start"))
        self.label_14.setText(_translate("Archiver", "End"))
        self.plotButton.setText(_translate("Archiver", "Plot"))
        self.label_11.setText(_translate("Archiver", "PV"))
        self.add_curve_button.setText(_translate("Archiver", "Add Curve"))
        self.remove_curve_button.setText(_translate("Archiver", "Remove Curve"))
        self.clear_curve_button.setText(_translate("Archiver", "Clear Curve"))
        self.remove_axis_button.setText(_translate("Archiver", "Remove Axis"))
        self.add_axis_button.setText(_translate("Archiver", "Add Axis"))
        self.pushButton1.setText(_translate("Archiver", "30s"))
        self.pushButton2.setText(_translate("Archiver", "1m"))
        self.pushButton4.setText(_translate("Archiver", "15m"))
        self.pushButton3.setText(_translate("Archiver", "5m"))
        self.pushButton8.setText(_translate("Archiver", "8h"))
        self.pushButton6.setText(_translate("Archiver", "1h"))
        self.pushButton7.setText(_translate("Archiver", "4h"))
        self.pushButton5.setText(_translate("Archiver", "30m"))
        self.pushButton12.setText(_translate("Archiver", "2w"))
        self.pushButton15.setText(_translate("Archiver", "YTD"))
        self.pushButton10.setText(_translate("Archiver", "2d"))
        self.pushButton14.setText(_translate("Archiver", "6M"))
        self.pushButton11.setText(_translate("Archiver", "1w"))
        self.pushButton16.setText(_translate("Archiver", "1Y"))
        self.pushButton13.setText(_translate("Archiver", "1M"))
        self.pushButton9.setText(_translate("Archiver", "1d"))
        self.label.setText(_translate("Archiver", "Plot Strategy:"))
        self.export_pushButton.setToolTip(_translate("Archiver", "<=2 weeks"))
        self.export_pushButton.setText(_translate("Archiver", "Export Raw Data"))
        self.export_plot_pushButton.setToolTip(_translate("Archiver", "<=2 weeks"))
        self.export_plot_pushButton.setText(_translate("Archiver", "Export Plot Data"))
        self.label_2.setText(_translate("Archiver", "Live:"))
        self.label_3.setText(_translate("Archiver", "Correlation:"))
