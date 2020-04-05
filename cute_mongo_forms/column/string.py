"""
string.py : Columns for restricted string data (ip addresses etc.)

* Copyright: 2018 Sampsa Riikonen
* Authors  : Sampsa Riikonen
* Date     : 2018
* Version  : 0.7.1

This file is part of the cute_mongo_forms library

License: LGPLv3+ (see the COPYING.LESSER file)
"""

import sys
# from PyQt5 import QtWidgets, QtCore, QtGui # Qt5
from PySide2 import QtWidgets, QtCore, QtGui
from cute_mongo_forms.tools import typeCheck, dictionaryCheck, objectCheck, parameterInitCheck, noCheck
from cute_mongo_forms.column.base import LineEditColumn, Column

pre_mod = "module.submodule : "  # a string for aux debuggin purposes


class IPv4AddressColumn(LineEditColumn):
    """A String restricted to IP address
    """
    # https://stackoverflow.com/questions/23166283/how-to-set-input-mask-and-qvalidator-to-a-qlineedit-at-a-time-in-qt

    parameter_defs = {
        "key_name": str,  # name of the database key in key(value)
        "label_name": str,  # used to create the forms
        "def_value": (str, "000.000.000.000")
    }
    parameter_defs.update(Column.parameter_defs)

    def makeWidget(self):
        self.widget = QtWidgets.QLineEdit()
        """ # (1) regexp validator
    ipRange = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])";
    # You may want to use QRegularExpression for new code with Qt 5 (not mandatory)
    ip_regex = QtCore.QRegExp("^" + ipRange
                 + "\\." + ipRange
                 + "\\." + ipRange
                 + "\\." + ipRange + "$")
    self.ip_validator = QtGui.QRegExpValidator(ip_regex)
    
    self.widget.setValidator(self.ip_validator)
    """
        # (2) input mask
        self.widget.setInputMask("000.000.000.000")

    def reset(self):
        self.setValue(self.def_value)



class FileDialogColumn(LineEditColumn):
    """Opens a file dialog
    """
    parameter_defs = {
        "key_name"   : str,  # name of the database key in key(value)
        "label_name" : str,  # used to create the forms
        "def_value"  : (str, ""),
        "filter"     : str
    }
    parameter_defs.update(Column.parameter_defs)

    def makeWidget(self):
        self.widget = QtWidgets.QWidget()
        self.lay = QtWidgets.QHBoxLayout(self.widget)

        self.line = QtWidgets.QLineEdit(self.widget)
        self.line.setReadOnly(True)

        self.button = QtWidgets.QPushButton("Choose", self.widget)
        self.lay.addWidget(self.line)
        self.lay.addWidget(self.button)

        self.button.clicked.connect(self.open_dialog_slot)


    def open_dialog_slot(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(filter = self.filter)[0]
        if not fname:
            pass
        else:
            self.setValue(fname)


    def getNotifySignal(self):
        return self.line.editingFinished


    def getValue(self):
        # Get the value from QtWidget
        return self.line.text()


    def setValue(self, txt):
        # Set the value of the QtWidget
        self.line.setText(str(txt))


    def reset(self):
        self.setValue(self.def_value)



