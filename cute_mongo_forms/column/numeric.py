"""
numeric.py : Columns for numeric data

* Copyright: 2018 [copyright holder]
* Authors  : Sampsa Riikonen
* Date     : 2018
* Version  : 0.1

This file is part of the cute_mongo_forms library

License: LGPLv3+ (see the COPYING.LESSER file)
"""

import sys
# from PyQt5 import QtWidgets, QtCore, QtGui # Qt5
from PySide2 import QtWidgets, QtCore, QtGui
from cute_mongo_forms.tools import typeCheck, dictionaryCheck, objectCheck, parameterInitCheck, noCheck
from cute_mongo_forms.column.base import LineEditColumn

pre_mod = "module.submodule : " # a string for aux debuggin purposes



class IntegerColumn(LineEditColumn):
  """Resticted integer column
  """
  
  parameter_defs={
    "key_name"   : str,  # name of the database key in key(value)
    "label_name" : str,  # used to create the forms
    "min_value"  : (int, 0),
    "max_value"  : (int, 65536),
    "def_value"  : (int, 0)
    }
    

  def makeWidget(self):
    self.validator = QtGui.QIntValidator(self.min_value, self.max_value)
    self.widget = QtWidgets.QLineEdit()
    self.widget.setValidator(self.validator)


  def getValue(self):
    # Get the value from QtWidget
    return int(self.widget.text())
  
  
  def setValue(self, i: int):
    # Set the value of the QtWidget
    assert(isinstance(i, int))
    self.widget.setText(str(i))
    
    
  def reset(self):
    self.setValue(self.def_value)



class ConstantIntegerColumn(IntegerColumn):
  """Restricted constant (not editable by the user) column
  """
  
  def makeWidget(self):
    super().makeWidget()
    self.widget.setReadOnly(True)
  
  
  
  



