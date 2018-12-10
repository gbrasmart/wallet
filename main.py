#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from pprint import pprint
from settings import Settings
from PyQt5.QtWidgets import QApplication
from widgets import keys, keygen, mainwindow, transactionsform, controllers



class Application(object):
    mainwindow = None
    transactions = None
    keygen = None
    keys = None
    settings = None

    m_mainController = None


    def __init__(self):
        self.settings = Settings()
        self.settings.load()

        self.keys = keys.Keys()
        self.keys.keysUseButton.clicked.connect(self.use_keys_clicked)
        self.keys.keysCancelButton.clicked.connect(self.exit_app)
        self.keys.keysGenButton.clicked.connect(self.show_gen_window)

        self.keygen = keygen.KeyGen()
        self.keygen.set_settings(self.settings)
        self.keygen.genKeysCancelButton.clicked.connect(self.gen_keys_cancel_clicked)
        self.keygen.genKeysGenButton.clicked.connect(self.gen_keys_gen_button_clicked)


        self.mainwindow = mainwindow.Ui_MainWindow()
        self.transactions = transactionsform.Ui_TransactionsForm()
        self.transactions.setupUi(self.transactions)


        # self.mainwindow = mainwindow.Ui_MainWindow()
        # self.transactions = transactionsform.Ui_TransactionsForm()
        # self.load_ini()

    def gen_keys_gen_button_clicked(self):
        if self.keygen.check_dir_filled():
            self.keygen.create_keys()
            if self.keygen.save_keys():
                self.keygen.close()
                self.start_main_window()

    def gen_keys_cancel_clicked(self):
        self.keygen.close()
        self.keys.show()

    def start_main_window(self):
        self.m_mainController = controllers.mainController(self.settings.public_key,
                                                           self.settings.private_key)
        self.mainwindow.controller = self.m_mainController
        self.mainwindow.setupUi(self.mainwindow)
        self.mainwindow.show()


    def show_keys_window(self):
        self.keys.show()

    def show_gen_window(self):
        self.keys.close()
        self.keygen.show()

    def use_keys_clicked(self):
        self.keys.read_key_files()
        if self.keys.keys_exists():
            self.keys.close()
            self.settings.private_key_file = self.keys.private_key_file
            self.settings.public_key_file = self.keys.public_key_file
            self.settings.save()
            self.show_main_window()



    def check_keys(self):
        if self.settings.private_key_file is not None \
            and self.settings.public_key_file is not None:
            self.keys.private_key_file = self.settings.private_key_file
            self.keys.public_key_file = self.settings.public_key_file
            self.keys.read_key_files()
            if self.keys.keys_exists():
                self.settings.private_key = self.keys.private_key
                self.settings.public_key = self.keys.public_key
                return True

        if self.settings.private_key is None \
            or self.settings.public_key is None:
            self.show_keys_window()
        return False

    def exit_app(self):
        sys.exit()

def main():
    qapp = QApplication(sys.argv)
    app = Application()

    key_check = app.check_keys()
    if key_check:
        pprint("k ok")
        app.start_main_window()


    sys.exit(qapp.exec_())


if __name__ == "__main__":
    main()
