"""
base.py    : Base/example classes for containers (lists, forms, etc.).  Containers use collections in various ways.

* Copyright: 2017-2018 Sampsa Riikonen
* Authors  : Sampsa Riikonen
* Date     : 2017
* Version  : 0.1

This file is part of the cute_mongo_forms library

License: LGPLv3+ (see the COPYING.LESSER file)
"""

import sys
# from PyQt5 import QtWidgets, QtCore, QtGui # Qt5
from PySide2 import QtWidgets, QtCore, QtGui
from cute_mongo_forms.tools import typeCheck, dictionaryCheck, objectCheck, parameterInitCheck, noCheck, Namespace
from cute_mongo_forms.row import RowWatcher
pre_mod = "container.base : " # a string for aux debugging purposes
# verbose=False # module's verbosity
verbose=True


class List:
  """Manages a QListWidget connected to a collection
  
  Parameters at instantiation:
  
  :param collection: Collection object with records corresponding to Row classes
  """
  
  parameter_defs={
    "collection"  : None
    }
  

  def __init__(self,**kwargs):
    self.pre=self.__class__.__name__+" : " # auxiliary string for debugging output
    parameterInitCheck(self.parameter_defs,kwargs,self) # check kwargs agains parameter_defs, attach ok'd parameters to this object as attributes
    self.makeWidget()
    self.update()
    self.clearSelection()
    
    
  def makeWidget(self):
    # Creates the root QtWidget.  Adds subwidgets.
    self.widget=QtWidgets.QListWidget()
    
    
  def createItem(self):
    """Overwrite in child classes to create custom items (say, sortable items, etc.)
    """
    return QtWidgets.QListWidgetItem()
    
    
  def update(self):
    # Fills the root and subwidgets with data.
    self.widget.clear()
    self.items_by_id={}
    for entry in self.collection.get():
      item  =self.createItem()
      label =self.makeLabel(entry)
      item.setText(label)
      item._id         =entry["_id"]
      try:
        item.classname =entry["classname"]
      except KeyError:
        raise(KeyError("Your database contains crap.  Do a purge"))
      self.items_by_id[item._id]=item
      self.widget.addItem(item)
    self.widget.sortItems()
      
      
  def makeLabel(self,entry):
    """How to create a label from a database record.  Overwrite in child classes.
    """
    return str(entry["_id"])
    
    
  def clearSelection(self):
    if (verbose): print(self.pre,"clearSelection")
    for _id in self.items_by_id:
      self.items_by_id[_id].setSelected(False)
    # self.widget.currentItemChanged.emit(None,None) # no way not to choose anything?
    
    
  def update_slot(self,_id):
    """Sending a signal to this slot updates the list.
    
    :param _id: Current item is set to this list item.  None = request clear selection.
    """
    if (verbose): print(self.pre,"update_slot",_id)
    self.update()
    
    try:
      item=self.items_by_id[_id] # no such record (probably deleted) #  TODO
    except KeyError:
      _id=None
      
    if (verbose): print(self.pre,"update_slot: _id=",_id)
      
    if (_id==None):
      self.clearSelection()
    else:
      self.widget.setCurrentItem(self.items_by_id[_id])
    


class SimpleForm:
    """Embed the widget of a Row into another widget (for including button, extra labels, etc.)
    """
  
    parameter_defs={
        "row_class" : RowWatcher
    }
  
    def __init__(self, **kwargs):
        self.pre=self.__class__.__name__+" : " # auxiliary string for debugging output
        parameterInitCheck(self.parameter_defs,kwargs,self) # check kwargs agains parameter_defs, attach ok'd parameters to this object as attributes
        self.row_instance = self.row_class()                
        self.makeWidget()
        
  
    def makeWidget(self):
        self.widget  = QtWidgets.QWidget()
        self.lay     = QtWidgets.QVBoxLayout(self.widget)
        self.row_instance.widget.setParent(self.widget)
        self.lay.addWidget(self.row_instance.widget)
        # subclass and continue from here to add buttons, etc
        
  
    
class FormSet:
  """Group of forms.  Each form corresponds to a different Row class.  Only one type of form is visible at a time.
  
  Parameters at instantiation:
    
  :param collection: Collection object with row classes and the document collection
  """
  
  parameter_defs={
    "collection"       : None
    }
  
  
  class Signals(QtCore.QObject):
    pass
    
  
  def __init__(self,**kwargs):
    self.pre=self.__class__.__name__+" : " # auxiliary string for debugging output
    parameterInitCheck(FormSet.parameter_defs,kwargs,self) # check kwargs agains parameter_defs, attach ok'd parameters to this object as attributes
    self.row_classes=self.collection.getRowClasses()
    self.signals=self.Signals()
    self.makeWidget()
    self.initVars()
    self.showCurrent()
  
  
  def initVars(self):
    self.element    =None # NoneType or QListWidgetItem with extra attributes "_id" and "classname" attached
    self.current_row=None


  def makeRows(self):
    # self.default_row_name=self.row_classes[0].__name__
    self.row_instance_by_name={}
    for row_class in self.row_classes:
      self.row_instance_by_name[row_class.__name__]=row_class() # each row has a widget attribute which is the root of the column qt widgets
    self.current_row=None


  def makeWidget(self):
    self.widget  =QtWidgets.QWidget()
    self.lay     =QtWidgets.QVBoxLayout(self.widget)
    self.makeForm()
    self.lay.addWidget(self.form)
  

  def makeForm(self):
    self.makeRows()
    self.form    =QtWidgets.QWidget(self.widget)
    self.form.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    self.form_lay=QtWidgets.QVBoxLayout(self.form)
    for key, row in self.row_instance_by_name.items():
      if (row.widget):
        row.widget.setParent(self.form)
        self.form_lay.addWidget(row.widget)
  
  
  def resetForm(self):
    for key, row in self.row_instance_by_name.items():
      if (row.widget):
        row.clear()
  
  
  def updateWidget(self):
    self.form.close()
    self.makeForm()
    self.chooseForm_slot(self.element,None)
    
    
  def showCurrent(self):
    # Hide all widgets, show just the one corresponding to current row
    if (verbose): print(self.pre,"showCurrent: current_row=",str(self.current_row))
    for key in self.row_instance_by_name:
      self.row_instance_by_name[key].widget.hide()
    if (type(self.current_row)==type(None)):
      pass
    else:
      self.current_row.widget.show()
    
  
  def chooseForm_slot(self,element,element_old):
    """Calling this slot chooses the form to be shown
    
    :param element:      an object that has *_id* and *classname* attributes
    :param element_old:  an object that has *_id* and *classname* attributes
    
    This slot is typically connected to List classes, widget attribute's, currentItemChanged method (List.widget is QListWidget that has currentItemChanged slot), so the element and element_old parameters are QListWidgetItem instances with extra attributes "_id" and "_classname" attached.
    
    Queries the database for element._id
    """
    if (verbose): print(self.pre,"chooseForm_slot :",element) # enable this if you're unsure what's coming here..
    if (type(element)==type(None)):
      self.current_row=None
      self.element    =None
    else:
      # print(self.pre,"chooseForm_slot :",element)
      assert(hasattr(element,"_id"))
      assert(hasattr(element,"classname"))
      try:
        self.current_row=self.row_instance_by_name[element.classname]
      except KeyError:
        print(self.pre,"chooseForm_slot : no such classname for this FormSet : ",element.classname)
        self.current_row=None
        self.element    =None
      else:
        self.current_row.get(self.collection,element._id)
        self.element=element
        
    self.showCurrent()
    
    
  def updateWidget_slot(self):
    self.updateWidget()
  
  
  
class RowDialog(QtWidgets.QDialog):
  
  
  def __init__(self,typenames,title="",parent=None):
    super().__init__(parent)
    self.setWindowTitle(title)
    
    self.layout=QtWidgets.QVBoxLayout(self)
    self.qlis  =QtWidgets.QListWidget(self)
    
    self.create=QtWidgets.QPushButton("Create",self)
    self.cancel=QtWidgets.QPushButton("Cancel",self)
    
    self.layout.addWidget(self.qlis)
    self.layout.addWidget(self.create)
    self.layout.addWidget(self.cancel)
    
    for typename in typenames:
      item=QtWidgets.QListWidgetItem()
      item.setText(typename)
      item.typename=typename
      self.qlis.addItem(item)
    
    self.create.clicked.connect(lambda: self.done(1))
    self.cancel.clicked.connect(lambda: self.reject())
    self.clear()
    
    
  def clear(self):
    # self.name.clear()
    pass
    
    
  def exec_(self):
    self.clear()
    i=super().exec_()
    item=self.qlis.currentItem()
    if (verbose):  print("NewRowDialogSimple: item=",item,"code=",i)
    if (i==0):
      return None
    else:
      return item.typename
  
  
  
class EditFormSet(FormSet):
  """Derived from FormSet.  Here we have, additionally, buttons for creating new records, and for copying, saving and clearing them.  This FormSet makes it possible to write into the collection.
  """
  
  class Signals(QtCore.QObject):
    """Signals emitted by this class:
    
    - new_record(object) : emitted when a new record has been added.  Carries the record _id.
    - save_record(object): emitted when a record has been saved.  Carries the record _id.
    """
    """
    new_record   =QtCore.pyqtSignal(object) # emitted when a new record has been added.  Sends the object id
    save_record  =QtCore.pyqtSignal(object) # emitted when a record has been saved
    delete_record=QtCore.pyqtSignal(object) # emitted when a record has been deleted
    modified     =QtCore.pyqtSignal(object) # emitted when one of the above has been triggered
    """
    new_record   =QtCore.Signal(object) # emitted when a new record has been added.  Sends the object id
    save_record  =QtCore.Signal(object) # emitted when a record has been saved
    delete_record=QtCore.Signal(object) # emitted when a record has been deleted
    modified     =QtCore.Signal(object) # emitted when one of the above has been triggered
  
  
  def makeWidget(self):
    self.widget=QtWidgets.QWidget()
    self.lay   =QtWidgets.QVBoxLayout(self.widget)
    self.makeForm() # from mother class
    self.lay.insertWidget(0,self.form)
    self.row_dialog =RowDialog(self.row_instance_by_name.keys())
    self.makeButtons()
    self.lay.insertWidget(1,self.buttons)
    
    
  def makeButtons(self):
    self.buttons =QtWidgets.QWidget(self.widget)
    self.buttons_lay =QtWidgets.QHBoxLayout(self.buttons)
    
    self.new_button   =QtWidgets.QPushButton ("NEW",    self.buttons)
    self.copy_button  =QtWidgets.QPushButton ("COPY",   self.buttons)
    self.save_button  =QtWidgets.QPushButton ("SAVE",   self.buttons)
    self.clear_button =QtWidgets.QPushButton ("CLEAR",  self.buttons)
    self.delete_button=QtWidgets.QPushButton ("DELETE", self.buttons)
    
    self.new_button.   clicked. connect(self.new_slot)
    self.copy_button.  clicked. connect(self.copy_slot)
    self.save_button.  clicked. connect(self.save_slot)
    self.clear_button. clicked. connect(self.clear_slot)
    self.delete_button.clicked. connect(self.delete_slot)
    
    self.buttons_lay.addWidget(self.new_button)
    self.buttons_lay.addWidget(self.copy_button)
    self.buttons_lay.addWidget(self.save_button)
    self.buttons_lay.addWidget(self.clear_button)
    self.buttons_lay.addWidget(self.delete_button)
    
    self.signals.new_record.   connect(self.signals.modified.emit)
    self.signals.save_record.  connect(self.signals.modified.emit)
    self.signals.delete_record.connect(self.signals.modified.emit)
    

  def updateWidget(self):
    self.form.close()
    self.makeForm()
    self.lay.insertWidget(0,self.form)
    self.chooseForm_slot(self.element,None)
    
  
  # *** internal slots ***
  def new_slot(self):
    res=self.row_dialog.exec_()
    if (type(res)==type(None)):
      return
    self.current_row=self.row_instance_by_name[res]
    self.showCurrent()
    self.current_row.clear()
    _id=self.current_row.new(self.collection)
    if (verbose): print(self.pre,"new_slot: _id=",_id)
    self.signals.new_record.emit(_id)
    
    
  def copy_slot(self):
    if (type(self.current_row)==type(None)):
      if (verbose): print(self.pre,"copy_slot : can't copy None")
    else:
      _id=self.current_row.new(self.collection)
      self.signals.new_record.emit(_id)
      
    
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
  
  
  def delete_slot(self):
    if (type(self.element)==type(None)):
      print(self.pre,"delete_slot : no document chosen yet")
      return
    if (verbose): print(self.pre,"delete_slot: self.element=",self.element)
    self.current_row.delete(self.collection,self.element._id)
    self.collection.save()
    self.signals.delete_record.emit(self.element._id)
    self.initVars()
    self.showCurrent()
    
  
  

class PermissionFormSet(EditFormSet):
  """A special FormSet derived from EditFormSet.  Links two tables together with foreign keys.
  
  :param collection: Database collection.  Database should have two foreign key columns
  :param key1_name:  Name of the column having the first foreign key
  :param key1_name:  Name of the column having the second foreign key
  """
  
  parameter_defs={
    "collection"       : None,
    "key1_name"        : str,   # collection should have two foreign key columns having these labels
    "key2_name"        : str
    }
  
  
  def __init__(self,**kwargs):
    self.pre=self.__class__.__name__+" : " # auxiliary string for debugging output
    parameterInitCheck(PermissionFormSet.parameter_defs,kwargs,self) # check kwargs agains parameter_defs, attach ok'd parameters to this object as attributes
    self.row_classes=self.collection.getRowClasses()
    self.signals=self.Signals()
    self.makeWidget()
    self.initVars()
  
  
  def makeButtons(self):
    self.buttons =QtWidgets.QWidget(self.widget)
    self.buttons_lay =QtWidgets.QHBoxLayout(self.buttons)
    
    self.new_button   =QtWidgets.QPushButton ("NEW",    self.buttons)
    self.save_button  =QtWidgets.QPushButton ("SAVE",   self.buttons)
    self.clear_button =QtWidgets.QPushButton ("CLEAR",  self.buttons)
    self.delete_button=QtWidgets.QPushButton ("DELETE", self.buttons)
    
    self.new_button.   clicked. connect(self.new_slot)
    self.save_button.  clicked. connect(self.save_slot)
    self.clear_button. clicked. connect(self.clear_slot)
    self.delete_button.clicked. connect(self.delete_slot)
    
    self.buttons_lay.addWidget(self.new_button)
    self.buttons_lay.addWidget(self.save_button)
    self.buttons_lay.addWidget(self.clear_button)
    self.buttons_lay.addWidget(self.delete_button)
    
    self.signals.new_record.   connect(self.signals.modified.emit)
    self.signals.save_record.  connect(self.signals.modified.emit)
    self.signals.delete_record.connect(self.signals.modified.emit)
  
  
  def initVars(self):
    self.element    =None   # something with "_id" and "classname" attributes
    self.current_row=None
    self.col1_key   =None
    self.col2_key   =None
  
  
  def setForm(self):
    if (verbose): print(self.pre,"setForm : ",self.col1_key,self.col2_key)
    if (self.col1_key!=None and self.col2_key!=None):
      row_query=self.collection.get(query={self.key1_name:self.col1_key,self.key2_name:self.col2_key}) # let's see if the collection has two foreign keys corresponding to requested values ..
      try:
        dic=next(row_query)
      except StopIteration:
        dic=None
    else:
      dic=None
      
    if (verbose): print(self.pre,"setForm : dic=",dic)
      
    # must go from dictionary to namespace .. remember that copy_slot, new_slot, etc. assume an object with "_id" and "classname" attributes
    if (type(dic)==type(None)):
      self.element=None
    else:
      self.element           =Namespace()
      self.element._id       =dic["_id"]
      self.element.classname =dic["classname"]
      
    if (type(self.element)==type(None)):
      self.current_row=None
    else:
      self.current_row=self.row_instance_by_name[self.row_classes[0].__name__] # assume just one row class ..
      self.current_row.set_(dic) # no need to query the database again (using Row.get).  Just set the values
      
    self.showCurrent()
  
  
  # *** internal slots ***
  def new_slot(self):
    self.current_row=self.row_instance_by_name[self.row_classes[0].__name__]
    self.showCurrent()
    self.current_row.clear()
    
    if (self.col1_key!=None and self.col2_key!=None):
      self.current_row[self.key1_name].setValue(self.col1_key)
      self.current_row[self.key2_name].setValue(self.col2_key)
    else:
      print(self.pre,"Must choose two columns")
      return
      
    _id=self.current_row.new(self.collection)
    
    if (verbose): print(self.pre,": new_slot : ",self.collection)
    
    self.setForm()
    self.signals.new_record.emit(_id)
    
    
  def save_slot(self):
    if (type(self.element)==type(None)):
      print(self.pre,"save_slot : no document chosen yet")
      return
    self.current_row.update(self.collection,self.element._id)
    self.collection.save()
    
    
  def clear_slot(self):
    if (type(self.current_row)==type(None)):
      print(self.pre,"clear_slot : can't clear None")
    else:
      self.current_row.clear()
  
  
  def delete_slot(self):
    if (type(self.element)==type(None)):
      print(self.pre,"delete_slot : no document chosen yet")
      return
    if (verbose): print(self.pre,"delete_slot: self.element=",self.element)
    self.current_row.delete(self.collection,self.element._id)
    self.collection.save()
    self.signals.delete_record.emit(self.element._id)
    self.initVars()
    self.showCurrent()
  
  
  
  # *** API slots ***
  def chooseRecord1_slot(self,element,element_old):
    """Calling this slot chooses the current record from the first collection
    
    :param element:      an object that has *_id* and *classname* attributes
    :param element_old:  an object that has *_id* and *classname* attributes
    """
    if (type(element)==type(None)):
      self.col1_key=None
    else:
      # print(self.pre,"chooseForm_slot :",element)
      assert(hasattr(element,"_id"))
      assert(hasattr(element,"classname"))
      # is this id in the permission table?
      self.col1_key=element._id
    self.setForm()
      
  
  def chooseRecord2_slot(self,element,element_old):
    """Calling this slot chooses the current record from the second collection
    
    :param element:      an object that has *_id* and *classname* attributes
    :param element_old:  an object that has *_id* and *classname* attributes
    """
    if (type(element)==type(None)):
      self.col2_key=None
    else:
      # print(self.pre,"chooseForm_slot :",element)
      assert(hasattr(element,"_id"))
      assert(hasattr(element,"classname"))
      # is this id in the permission table?
      self.col2_key=element._id
    self.setForm()
    
  

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

