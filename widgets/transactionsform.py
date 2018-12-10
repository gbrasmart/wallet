#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pprint import pprint
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TransactionsForm(QtWidgets.QDialog):
    def setupUi(self, TransactionsForm):
        TransactionsForm.setObjectName("TransactionsForm")
        TransactionsForm.resize(1024, 768)
        self.tableWidget = QtWidgets.QTableWidget(TransactionsForm)
        self.tableWidget.setEnabled(True)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 1005, 748))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tableWidget.setAutoFillBackground(False)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setKerning(True)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(150)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        self.retranslateUi(TransactionsForm)
        QtCore.QMetaObject.connectSlotsByName(TransactionsForm)



    def retranslateUi(self, TransactionsForm):
        _translate = QtCore.QCoreApplication.translate
        TransactionsForm.setWindowTitle(_translate("TransactionsForm", "Form"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("TransactionsForm", "Amount"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("TransactionsForm", "Source"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("TransactionsForm", "Target"))

    def setTransactions(self, transactionsList=None):
        for t in transactionsList:
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            numcols = self.tableWidget.columnCount()
            numrows = self.tableWidget.rowCount()
            self.tableWidget.setRowCount(numrows)
            self.tableWidget.setColumnCount(numcols)
            amount = "{}.{} {}".format(t.amount.integral, t.amount.fraction, t.currency)
            self.tableWidget.setItem(numrows -1,0,QtWidgets.QTableWidgetItem(amount))
            self.tableWidget.setItem(numrows -1,1,QtWidgets.QTableWidgetItem(t.source))
            self.tableWidget.setItem(numrows -1,2,QtWidgets.QTableWidgetItem(t.target))
