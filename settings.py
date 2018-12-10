#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtCore import QSettings


class Settings(object):
    qsettings = None
    settings_file = None
    host = None
    port = None
    keys_dir = None
    public_key = None
    public_key_file = None
    private_key = None
    private_key_file = None

    def __init__(self):
        pass

    def load(self, filename=None):
        if filename is None:
            self.settings_file = 'settings.ini'
        else:
            self.settings_file = filename
        self.qsettings = QSettings(self.settings_file, QSettings.IniFormat)
        self.qsettings.setIniCodec("utf-8")
        self.qsettings.beginGroup("Node")
        if self.qsettings.value("host") is not None:
            self.host = self.qsettings.value("host")
        if self.qsettings.value("port") is not None:
            self.port = int(self.qsettings.value("port"))
        if self.qsettings.value("keys_dir") is not None:
            self.keys_dir = self.qsettings.value("keys_dir")
        if self.qsettings.value("private_key_file") is not None:
            self.private_key_file = self.qsettings.value("private_key_file")
        if self.qsettings.value("public_key_file") is not None:
            self.public_key_file = self.qsettings.value("public_key_file")
        self.qsettings.endGroup()
        self.qsettings.sync()

    def save(self):
        self.qsettings.beginGroup("Node")
        self.qsettings.setValue('host', self.host)
        self.qsettings.setValue('port', self.port)
        self.qsettings.setValue('public_key_file', self.public_key_file)
        self.qsettings.setValue('private_key_file', self.private_key_file)
        self.qsettings.endGroup()
        self.qsettings.sync()
