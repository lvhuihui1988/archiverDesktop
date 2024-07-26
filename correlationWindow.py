# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'correlationWindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_correlation(object):
    def setupUi(self, correlation):
        correlation.setObjectName("correlation")
        correlation.resize(1600, 800)
        correlation.setStyleSheet("background-color: rgb(239, 239, 239);")
        self.verticalLayoutWidget = QtWidgets.QWidget(correlation)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(40, 50, 1521, 721))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.retranslateUi(correlation)
        QtCore.QMetaObject.connectSlotsByName(correlation)

    def retranslateUi(self, correlation):
        _translate = QtCore.QCoreApplication.translate
        correlation.setWindowTitle(_translate("correlation", "Correlation Plot"))
