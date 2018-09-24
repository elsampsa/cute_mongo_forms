"""
base.py    : Basic column classes

* Copyright: 2017-2018 Sampsa Riikonen
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
pre_mod = "cute_mongo_forms.column.base : " # a string for aux debuggin purposes



class Column:
  """Mother class for columns.  Derive your own column class from this.  The column class encapsulates a particular QWidget and restrictions on the QWidget (through Qt input masks) of the accepted values.  The Row class uses Columns to read/set their values from/to a key-value document.
  
  Parameters at instantiation:
  
  :param key_name:  The key to be used in the key/value pair of the document database
  """
  
  parameter_defs={
    "key_name"   : str,  # name of the database key in key(value)
    "label_name" : str   # used to create the forms
    }

    
  def __init__(self,**kwargs):
    self.pre=self.__class__.__name__+" : " # auxiliary string for debugging output
    parameterInitCheck(self.parameter_defs,kwargs,self) # check kwargs agains parameter_defs, attach ok'd parameters to this object as attributes
    self.makeWidget()
    self.reset()
    

  def makeWidget(self):
    """For child classes, set the QtWidget here
    """
    raise(AssertionError("Virtual method"))
    

  def getValue(self):
    """Get the value from QtWidget
    """
    return None
  
  
  def setValue(self,txt): # the value (in key(value))
    """Set the value of the QtWidget
    """
    return None
    
    
  def setParent(self,parent):
    """Parent the QtWidget
    """
    self.widget.setParent(parent)
    
    
  def reset(self):
    """Set the column to its default empty value
    """
    pass
    
    
  def updateWidget(self):
    """This is for columns classes that have relations to a "foreign" collection (foreign keys).  Check the foreign collection and keep values in the widget consistent.
    """
    pass
  
  
  def purge(self, value):
    """Check if value is ok for this column.  If update is needed, return (True, updated_value), otherwise (False, original_value)
    """
    return False, value


  def getNotifySignal(self):
    """A notifying signal when this columns contents are changed
    """
    return None

  
class LineEditColumn(Column):
  """Derived from Column.  Unrestricted input text.
  """
  
  parameter_defs={
    "key_name"   : str,  # name of the database key in key(value)
    "label_name" : str   # used to create the forms
    }
    
  def __init__(self,**kwargs):
    self.pre=self.__class__.__name__+" : " # auxiliary string for debugging output
    parameterInitCheck(self.parameter_defs,kwargs,self) # check kwargs agains parameter_defs, attach ok'd parameters to this object as attributes
    self.makeWidget()
    self.reset()


  def makeWidget(self):
    self.widget=QtWidgets.QLineEdit()


  def getNotifySignal(self):
    return self.widget.editingFinished
  

  def getValue(self):
    # Get the value from QtWidget
    return self.widget.text()
  
  
  def setValue(self,txt):
    # Set the value of the QtWidget
    self.widget.setText(str(txt))
    
    
  def reset(self):
    self.setValue("")
    
    
    
class LabelColumn(Column):
  """Column that does not create a key-value pair.  No data here, just a label
  
  TODO: experimental, dont use
  """
  parameter_defs={
    "label_name" : str
  }
  
  def __init__(self,**kwargs):
    self.pre=self.__class__.__name__+" : " # auxiliary string for debugging output
    parameterInitCheck(self.parameter_defs,kwargs,self) # check kwargs agains parameter_defs, attach ok'd parameters to this object as attributes
    self.makeWidget()
    self.reset()


  def makeWidget(self):
    self.widget=QtWidgets.QLabel(self.label_name)


  def getValue(self):
    # Get the value from QtWidget
    return None
  
  
  def setValue(self,txt):
    # Set the value of the QtWidget
    pass
    
  def reset(self):
    pass
  
  
  
class ComboBoxColumn(Column):
  """A Column that can have a finite number of different values.  The possible values are defined in a specific collection that is given as a parameter (let's call this "foreign collection").  The element in the QtWidget form corresponding to this column is a drop-down list (e.g. a QComboBox).
  
  The collection schema looks like this:
  
  ::
  
      principal collection          foreign collection
      --------------------          ------------------
      _id                     +---> _id
      key1                    |     label
      key2            --------+  
      key2
      --------------------          ------------------
  
  
  Parameters at instantiation:
  
  :param collection:            Foreign collection that has all possible values for the drop-down list
  :param key_name:              Key in the principal collection whose values correspond to keys in the foreign collection (in that example above key_name = key2)
  :param label_name:            Name of the drop-down list in the form widget
  :param foreign_label_name:    Name of the key in the foreign collection for a value shown in the pricipal collection.  Default: "label"
  :param foreign_key_name:      Name of the foreign key in the foreign collection.  Default: "_id"
  """
  
  # define here, where the foreign key is mapped..
  parameter_defs={
    "collection" : None,
    "key_name"   : str,  # name of the database key in key(value)
    "label_name" : str,  # used to create the forms
    "foreign_label_name" : (str,"label"),  # label corresponding to this foreign key
    "foreign_key_name"   : (str,"_id")     # by default, use the object id as the foreign key
    }
  
  
  def __init__(self,**kwargs):
    self.pre=self.__class__.__name__+" : " # auxiliary string for debugging output
    parameterInitCheck(self.parameter_defs,kwargs,self) # check kwargs agains parameter_defs, attach ok'd parameters to this object as attributes
    self.makeWidget()
    self.reset()

  
  def makeWidget(self):
    self.widget=QtWidgets.QComboBox()
    self.updateWidget()
    
    
  def updateWidget(self):
    self.widget.clear()
    it=self.collection.get()
    for i, item in enumerate(it):
      self.widget.insertItem(i,item[self.foreign_label_name],item[self.foreign_key_name])
    
      
  def getValue(self):
    # Get the value from QtWidget
    # self.widget.currenText()
    # self.widget.currentData()
    return self.widget.currentData() # returns the foreign key
  
  
  def setValue(self,foreign_key):
    # TODO: check that invalid foreign_key values are silently omitted
    # Set the value of the QtWidget
    # if foreign_key is not found (i.e. the row that's using this column has a database having incorrect foreign_key values),
    # findData returns -1
    # setCurrentIndex(-1) sets the selection to void
    i=self.widget.findData(foreign_key)
    self.widget.setCurrentIndex(i)
    
    
  def reset(self):
    self.widget.setCurrentIndex(-1)
    
    

class ForeignKeyColumn(Column):
  """A column that is a foreign key, referenced by another collection.  Does not create any visible widget into forms.  Basically, creates a key-value pair in the collection Row schema.  Does not know anything about mapping the key to a foreign table.
  
  Parameters at instantiation:
  
  :param key_name:         name of the key
  :param collection:       the "foreign" collection
  :param foreign_key_name: the key in the foreign collection (default: "_id")
  """
    
  parameter_defs={
    "key_name"           : str,        # database key in key(value)
    "collection"         : None,       # the "foreign" collection,
    "foreign_key_name"   : (str,"_id") # by default, use the object id as the foreign key
    }
  
  
  def __init__(self,**kwargs):
    self.pre=self.__class__.__name__+" : " # auxiliary string for debugging output
    parameterInitCheck(self.parameter_defs,kwargs,self) # check kwargs agains parameter_defs, attach ok'd parameters to this object as attributes
    self.makeWidget()
    self.reset()

  
  def makeWidget(self):
    self.widget=None # does not create any visible widget
    
    
  def getValue(self):
    # Get the value
    return self.value
    
  
  def setValue(self,value):
    # Set the value
    self.value=value
    
    
  def reset(self):
    self.value=None



class CheckBoxColumn(Column):
  """A column having a Qt checkbox and true/false value.
  """
  
  # define here, where the foreign key is mapped..
  parameter_defs={
    "key_name"   : str,  # name of the database key in key(value)
    "label_name" : str   # used to create the forms
    }
  
  
  def __init__(self,**kwargs):
    self.pre=self.__class__.__name__+" : " # auxiliary string for debugging output
    parameterInitCheck(self.parameter_defs,kwargs,self) # check kwargs agains parameter_defs, attach ok'd parameters to this object as attributes
    self.makeWidget()
    self.reset()

  
  def makeWidget(self):
    self.widget=QtWidgets.QCheckBox()
    
    
  def getValue(self):
    # Get the value from QtWidget
    return self.widget.isChecked()
    
  
  def setValue(self,val):
    # Set the value of the QtWidget
    self.widget.setChecked(val)
    
    
  def reset(self):
    self.setValue(False)



class ListEditColumn(Column):
  """A Column that is a list.  Possible values for the list element are defined in a specific collection that is given as a parameter (let's call this "foreign collection").  The element in the QtWidget form corresponding to this column is a QListWidget.  The GUI user can enable/check several values.  All these values are saved into the list.
  
  The collection schema looks like this:
  
  ::
  
      principal collection          foreign collection
      --------------------          ------------------
      _id                     +---> _id
      key1                    |     label
      key2: a list   --------+  
      key2
      --------------------          ------------------
  
  
  Parameters at instantiation:
  
  :param collection:            Foreign collection that has all possible values present in the list
  :param key_name:              Key in the principal collection whose values correspond to keys in the foreign collection (in that example above key_name = key2)
  :param label_name:            Name of the list in the form widget
  :param foreign_label_name:    Name of the key in the foreign collection for a value shown in the pricipal collection.  Default: "label"
  :param foreign_key_name:      Name of the foreign key in the foreign collection.  Default: "_id"
  """
  
  # define here, where the foreign key is mapped..
  parameter_defs={
    "collection" : None,
    "key_name"   : str,  # name of the database key in key(value)
    "label_name" : str,  # used to create the forms
    "foreign_label_name" : (str,"label"),  # label corresponding to this foreign key
    "foreign_key_name"   : (str,"_id")     # by default, use the object id as the foreign key
    }
  
  
  def __init__(self,**kwargs):
    self.pre=self.__class__.__name__+" : " # auxiliary string for debugging output
    parameterInitCheck(self.parameter_defs,kwargs,self) # check kwargs agains parameter_defs, attach ok'd parameters to this object as attributes
    self.makeWidget()
    self.reset()

  
  def makeWidget(self):
    self.widget=QtWidgets.QListWidget()
    self.widget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
    self.updateWidget()
    
      
  def getValue(self):
    # TODO: check that invalid values are silently omitted
    # Returns list of keys corresponding to selected elements
    lis=[]
    for el in self.widget.selectedItems():
      lis.append(el.key)
    return lis
    
    
  def setValue(self,key_list):
    # Selects elements in the list, based on key list
    for el in self.items:
      if (el.key in key_list):
        el.setSelected(True)
      else:
        el.setSelected(False)
      
    
  def updateWidget(self):
    self.widget.clear()
    self.items=[]
    it=self.collection.get()
    for i, item in enumerate(it):
      el=QtWidgets.QListWidgetItem()
      el.setText(item[self.foreign_label_name])
      el.key=item[self.foreign_key_name] # attach an extra attribute
      self.widget.addItem(el)
      self.items.append(el)
    
    
  def reset(self):
    for item in self.items:
      item.setSelected(False)
    
    

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

