#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pprint import pprint
import sys
from PyQt5.QtWidgets import QFileDialog, QWidget, QMessageBox
from PyQt5 import uic

class Keys(QWidget):
    private_key_file = None
    public_key_file = None
    private_key = None
    public_key = None

    def __init__(self):
        super().__init__()
        uic.loadUi("widgets/keys.ui", self)
        self.privKeyButton.clicked.connect(self.privKeyButton_clicked)
        self.pubKeyButton.clicked.connect(self.pubKeyButton_clicked)
        # self.keysUseButton.clicked.connect(self.keysUseButton_clicked)

    def privKeyButton_clicked(self):
        self.openFileNameDialog("private")

    def pubKeyButton_clicked(self):
        self.openFileNameDialog("public")

    # def keysUseButton_clicked(self):
    #     self.read_key_files()
    #     # TODO: close window, go to mainwindow


    def openFileNameDialog(self, key_type):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            "QFileDialog.getOpenFileName()",
            "","All Files (*);;Keys (*.key)",
            options=options
        )
        if fileName:
            print(fileName)
            if key_type == "private":
                self.private_key_file = fileName
                self.privKeyInput.setText(self.private_key_file)
            if key_type == "public":
                self.public_key_file = fileName
                self.pubKeyInput.setText(self.public_key_file)

    def read_key_files(self):
        try:
            with open(self.private_key_file, 'r') as r:
                self.private_key = r.read()
                r.close()
            with open(self.public_key_file, 'r') as r:
                self.public_key = r.read()
                r.close()
        except Exception as e:
            self.showdialog("Error reading key files")

        if self.private_key is not None and self.public_key is not None and \
            len(self.private_key) != 128 and len(self.public_key) != 64:
            self.showdialog("Invalid key files")

    def keys_exists(self):
        if self.private_key is not None and self.public_key is not None and \
            len(self.private_key) == 128 and len(self.public_key) == 64:
            return True
        return False

    def showdialog(self, text=None):
       msg = QMessageBox()
       msg.setIcon(QMessageBox.Information)
       msg.setText(text)
       msg.setWindowTitle("Error")
       msg.setStandardButtons(QMessageBox.Ok)
       msg.exec_()

