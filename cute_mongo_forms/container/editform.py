"""
editform.py : Yet more editable forms

* Copyright: 2018 Sampsa Riikonen
* Authors  : Sampsa Riikonen
* Date     : 2017
* Version  : 0.1

This file is part of the cute_mongo_forms library

License: LGPLv3+ (see the COPYING.LESSER file)
"""

import sys
# from PyQt5 import QtWidgets, QtCore, QtGui # Qt5
from PySide2 import QtWidgets, QtCore, QtGui
from cute_mongo_forms.tools import typeCheck, dictionaryCheck, objectCheck, parameterInitCheck, noCheck
from cute_mongo_forms.container.base import FormSet

pre_mod = "container.editform : " # a string for aux debuggin purposes
verbose = True

class EditFormSet2(FormSet):
  """Derived from FormSet.  Includes a drop-down menu for choosing the correct object class.
  """
  
  class Signals(QtCore.QObject):
    """Signals emitted by this class:
    
    - new_record(object) : emitted when a new record has been added.  Carries the record _id.
    - save_record(object): emitted when a record has been saved.  Carries the record _id.
    """
    save_record  =QtCore.Signal(object) # emitted when a record has been saved
    modified     =QtCore.Signal(object) # emitted when one of the above has been triggered
  
  
  def makeWidget(self):
    self.widget=QtWidgets.QWidget()
    self.lay   =QtWidgets.QVBoxLayout(self.widget)
    self.makeForm() # from mother class
    self.dropdown_widget=QtWidgets.QComboBox(self.widget)
    
    self.row_instance_by_index = []
    for i, key in enumerate(self.row_instance_by_name.keys()):
      row_instance = self.row_instance_by_name[key]
      self.row_instance_by_index.append(row_instance)
      classname = key
      display_name = row_instance.getName()
      self.dropdown_widget.insertItem(i, display_name)
    
    self.dropdown_widget.currentIndexChanged.connect(self.dropdown_changed_slot)
    
    self.lay.insertWidget(0,self.dropdown_widget)
    self.lay.insertWidget(1,self.form)
    self.makeButtons()
    self.lay.insertWidget(2,self.buttons)
    
    
  def makeButtons(self):
    self.buttons =QtWidgets.QWidget(self.widget)
    self.buttons_lay =QtWidgets.QHBoxLayout(self.buttons)
    
    self.save_button  =QtWidgets.QPushButton ("SAVE",   self.buttons)
    self.clear_button =QtWidgets.QPushButton ("CLEAR",  self.buttons)
    
    self.save_button.  clicked. connect(self.save_slot)
    self.clear_button. clicked. connect(self.clear_slot)
    
    self.buttons_lay.addWidget(self.save_button)
    self.buttons_lay.addWidget(self.clear_button)
    
    self.signals.save_record.  connect(self.signals.modified.emit)
    

  def showCurrent(self):
    # Hide all widgets, show just the one corresponding to current row
    if (verbose): print(self.pre,"showCurrent: current_row=",str(self.current_row))
    if (type(self.current_row)==type(None)):
      return
    i = self.row_instance_by_index.index(self.current_row)
    self.dropdown_widget.setCurrentIndex(i)
    self.dropdown_changed_slot(i)


  def updateWidget(self):
    self.form.close()
    self.makeForm()
    self.lay.insertWidget(0,self.form)
    self.chooseForm_slot(self.element,None)
    
  
  # *** internal slots ***
  def dropdown_changed_slot(self, i):
    print(self.pre,"dropdown_changed_slot",i,self.row_instance_by_index[i])
    for key in self.row_instance_by_name:
      self.row_instance_by_name[key].widget.hide()
  
    self.current_row = self.row_instance_by_index[i]
    if (type(self.current_row)==type(None)):
      pass
    else:
      self.current_row.widget.show()

  
  def save_slot(self):
    if (type(self.element)==type(None)):
      if (verbose): print(self.pre,"save_slot : no document chosen yet")
      return
    self.current_row.update(self.collection,self.element._id)
    self.collection.save()
    if (verbose): print(self.pre,"save_slot: emitting",self.element._id)
    self.signals.save_record.emit(self.element._id)
    
    
  def clear_slot(self):
    if (type(self.current_row)==type(None)):
      if (verbose): print(self.pre,"clear_slot : can't clear None")
    else:
      self.current_row.clear()
  
    
def test1():
  st="""Empty test
  """
  pre=pre_mod+"test1 :"
  print(pre,st)
  

def test2():
  st="""Empty test
  """
  pre=pre_mod+"test2 :"
  print(pre,st)
  

def main():
  pre=pre_mod+"main :"
  print(pre,"main: arguments: ",sys.argv)
  if (len(sys.argv)<2):
    print(pre,"main: needs test number")
  else:
    st="test"+str(sys.argv[1])+"()"
    exec(st)
  
  
if (__name__=="__main__"):
  main()

