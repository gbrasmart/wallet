#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pprint import pprint
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QSystemTrayIcon, QStyle, QAction, QMenu, qApp
from widgets import transactionsform
from widgets.icon import icon_data

from node import client


#TODO transaction class


class Ui_MainWindow(QtWidgets.QMainWindow):
    tray_icon = None
    window_size = None
    controller = None # mainWindow Controller




    #TODO make from window size
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("RaWallet")
        MainWindow.resize(485, 186)
        MainWindow.setMinimumSize(QtCore.QSize(485, 186))
        MainWindow.setMaximumSize(QtCore.QSize(485, 186))

        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")

        self.formLayoutWidget = QtWidgets.QWidget(self.centralWidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 451, 131))
        self.formLayoutWidget.setObjectName("formLayoutWidget")

        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(11, 11, 11, 11)
        self.formLayout.setSpacing(6)
        self.formLayout.setObjectName("formLayout")

        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")

        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.lineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit.setMinimumSize(QtCore.QSize(380, 0))
        self.lineEdit.setObjectName("lineEdit")

        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
        self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_2.setMinimumSize(QtCore.QSize(380, 0))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_2)
        self.label_5 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_5.setObjectName("label_5")

        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.lineEdit_3 = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_3.setMinimumSize(QtCore.QSize(300, 0))
        self.lineEdit_3.setObjectName("lineEdit_3")

        self.horizontalLayout.addWidget(self.lineEdit_3)

        self.pushButton_2 = QtWidgets.QPushButton(self.formLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")

        self.horizontalLayout.addWidget(self.pushButton_2)
        self.formLayout.setLayout(2, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label)
        self.label_4 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_4.setMinimumSize(QtCore.QSize(184, 0))
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.label_4)

        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralWidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 130, 460, 41))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.pushButton_3 = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_2.addWidget(self.pushButton_3)
        MainWindow.setCentralWidget(self.centralWidget)
        self.actionquit = QtWidgets.QAction(MainWindow)
        self.actionquit.setObjectName("actionquit")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(icon_data())
        tIcon = QtGui.QIcon()
        tIcon.addPixmap(pixmap)

        self.tray_icon = QSystemTrayIcon(self)
        # self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_DesktopIcon))
        # self.tray_icon.setIcon(QtGui.QIcon("src/main/icons/base/256.png"))
        self.tray_icon.setIcon(tIcon)

        show_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        show_action.triggered.connect(self.show)
        quit_action.triggered.connect(qApp.quit)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        self.pushButton.clicked.connect(self.balance_clicked)
        self.pushButton_2.clicked.connect(self.send_clicked)
        self.pushButton_3.clicked.connect(self.txs_clicked)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "pyWallet"))
        self.label_2.setText(_translate("MainWindow", "Source:"))
        self.label_3.setText(_translate("MainWindow", "Target:"))
        self.label_5.setText(_translate("MainWindow", "Amount:"))
        self.pushButton_2.setText(_translate("MainWindow", "Send"))
        self.label.setText(_translate("MainWindow", "Balance:"))
        self.label_4.setText(_translate("MainWindow", "0.0"))
        self.pushButton.setText(_translate("MainWindow", "Update Balance"))
        self.pushButton_3.setText(_translate("MainWindow", "View Transactions"))
        self.actionquit.setText(_translate("MainWindow", "Quit"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))

    def showdialog(self, text=None):
       msg = QtWidgets.QMessageBox()
       msg.setIcon(QtWidgets.QMessageBox.Information)
       msg.setText(text)
       msg.setWindowTitle("Error")
       msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
       msg.exec_()


    def balance_clicked(self):
        err = self.controller.network_connected()
        if err != None:
            self.showdialog(str(err))
            return
        balance = self.controller.get_balance()
        balanceStr = "{}.{}".format(balance.amount.integral, balance.amount.fraction)
        self.label_4.setText(balanceStr)


    def send_clicked(self):
        targetText = self.lineEdit_2.text()
        if len(targetText) == 0:
            self.showdialog("invalid Target format")
            return
        amountText = self.lineEdit_3.text()
        splits = amountText.split(".")
        if len(splits) != 2:
            self.showdialog("invalid Amount format")
            self.lineEdit_3.setText("")
            return
        try:
            amountIntegral = int(splits[0])
            amountFraction = int(splits[1])
        except Exception:
            self.showdialog("invalid Amount format")
            self.lineEdit_3.setText("")
            return

        err = self.controller.network_connected()
        if err != None:
            self.showdialog(str(err))
            return
        ok = self.controller.send_transaction(targetText,
                                              amountIntegral,amountFraction)

        if ok != None:
            self.showdialog("Transaction sent")
            self.lineEdit_2.setText("")
            self.lineEdit_3.setText("")
        else:
            self.showdialog("Transaction wasnt sent")


    #TODO rewrite btn_clicked

    #Not interesting now
    def txs_clicked(self):
        err = self.controller.network_connected()
        if err != None:
            self.showdialog(str(err))
            return
        txsResult = self.controller


        self.dialog = transactionsform.Ui_TransactionsForm()
        self.dialog.setupUi(self.dialog)
        if len(txsResult.transactions) > 0:
            self.dialog.setTransactions(txsResult.transactions)
        self.dialog.show()


    # Переопределение метода closeEvent, для перехвата события закрытия окна
    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "Rasmart-Wallet Program",
            "You can find Rasmart-Wallet in tray",
            QSystemTrayIcon.Information,
            500
        )



