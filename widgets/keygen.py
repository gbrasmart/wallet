#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from pprint import pprint
from PyQt5.QtWidgets import QWidget, QFileDialog, QMessageBox
from PyQt5 import uic
from ctypes import *
from sys import platform
from os import path
import os
import racrypt


class KeyGen(QWidget):
    library = None
    private_key = None
    public_key = None
    private_key_hex = None
    public_key_hex = None
    private_key_name = 'private.key'
    public_key_name = 'public.key'
    keys_dir = None
    settings = None

    def __init__(self):
        super().__init__()
        uic.loadUi("widgets/keysgen.ui", self)
        self.load_shared()
        self.genKeysSetDirButton.clicked.connect(self.gen_keys_dir_button_clicked)

    def set_settings(self, settings):
        self.settings = settings

    def check_dir_filled(self):
        dir = self.genKeysDirInput.text()
        if dir == "":
            self.showdialog("Please, choose keys directory")
            return False
        self.keys_dir = self.genKeysDirInput.text()
        return True

    def gen_keys_dir_button_clicked(self):
        self.openFileNameDialog()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dirname = QFileDialog.getExistingDirectory(self, "Select Directory")
        if dirname:
            self.genKeysDirInput.setText(dirname)

    def load_shared(self):
        self.library = racrypt.RaCryptLib()
        self.library.load(os.path.dirname(racrypt.__path__[0]))

    def create_keys(self):
        result = self.library.create_keys()
        self.public_key = self.library.public_key
        self.public_key_hex = self.library.public_key_hex
        self.private_key = self.library.private_key
        self.private_key_hex = self.library.private_key_hex
        return result

    def save_keys(self):
        if self.keys_dir is None:
            return False
        k_path_private = path.join(self.keys_dir, self.private_key_name)
        k_path_public = path.join(self.keys_dir, self.public_key_name)
        try:
            self.save_to_file(k_path_private, self.private_key_hex)
            self.save_to_file(k_path_public, self.public_key_hex)
            self.settings.private_key_file = k_path_private
            self.settings.public_key_file = k_path_public
            self.settings.save()
            return True
        except Exception as e:
            self.showdialog(str(e))
            return False

    def save_to_file(self, filename, content):
        mode = 'w'
        if isinstance(content, bytes):
            mode = 'wb'
        with open(filename, mode) as w:
            w.write(content)
            w.close()

    def showdialog(self, text=None):
       msg = QMessageBox()
       msg.setIcon(QMessageBox.Information)
       msg.setText(text)
       msg.setWindowTitle("Error")
       msg.setStandardButtons(QMessageBox.Ok)
       msg.exec_()

