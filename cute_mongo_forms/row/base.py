"""
base.py    : The Row class

* Copyright: 2017-2018 Sampsa Riikonen
* Authors  : Sampsa Riikonen
* Date     : 2017
* Version  : 0.1

This file is part of the cute_mongo_forms library

License: LGPLv3+ (see the COPYING.LESSER file)
"""

# from PyQt5 import QtWidgets, QtCore, QtGui # Qt5
from PySide2 import QtWidgets, QtCore, QtGui
import sys
import copy
import collections
from cute_mongo_forms.tools import typeCheck, dictionaryCheck, objectCheck, parameterInitCheck, noCheck
from cute_mongo_forms.column.base import Column, LineEditColumn
pre_mod = "cute_mongo_forms.row.base : " # a string for aux debuggin purposes
verbose=False # module's verbosity


class ColumnSpec:
  
  def __init__(self,column_class,**kwargs):
    self.column_class=column_class
    self.kwargs      =kwargs
    
    
  def instantiate(self):
    return self.column_class(**self.kwargs)
    
    
    
class RowWatcher(type):
  def __init__(cls, name, bases, clsdict):
    if len(cls.mro()) > 2:
      # print("was subclassed by " + name +" "+cls.__name__)
      cls.genKeys()
      # print(cls.keys)
    super(RowWatcher, cls).__init__(name, bases, clsdict)
  
    

class Row(metaclass=RowWatcher):
  """
  Defines a common columns structure for documents in a [document database] collection.  The column structure (i.e. "Row") is defined in the child class header like this:
  
  ::
  
    columns=[
      ColumnSpec(LineEditColumn, key_name="firstname", label_name="First Name"),
      ...
    ]
  
  This class knows how to create a Qt form, corresponding to the column structure
  """
  name=None # if not defined, use classes __name__ attribute
  columns=[]
  
  parameter_defs={}
  
  keys=[]       # filled by first call to getKeys
  keyset=None   # re-generated each time you call "class Classname(Row) ..".  Why this?  We need the "keyset" at class level, not at object level
  
  
  @classmethod
  def genKeys(cls):
    """This is called when you declare the class, i.e. at "Class MyNewRow(Row) ...".  It updates the class variables "keys" and "keyset"
    """
    cls.keys=[]
    for col in cls.columns: # ColumnSpec instances 
      if ("key_name" in col.kwargs):
        cls.keys.append(col.kwargs["key_name"]) # remember.. ColumnSpec has kwargs thats going to be passed to each column when they're instantiated.  "key_name" has the name of the column key.
    cls.keyset=set(cls.keys)
      
      
  @classmethod
  def genChecker(cls):
    pass
    """ # TODO associated "orm" class for programmatic (i.e. non-widget) manipulation of the underlying database: we want to check that what we write to database is correct
  
    class RowCheck: # 
  
      def __init__(self):
        for col in cls.columns:
            pass
        # or ..
        for key, column in column_by_name.items()
          self.column_check_by_name[key] =column.ColumnCheck() # ColumnCheck instance.  Houses a copy of the value.
        
        
      def __getattr__(self,key):
        # classname and _id must be handled separately
        # _id is saved as an attribute of RowCheck
        # classname should be a constant
        column_check=self.column_check_by_name[key]
        return column_check.get()
      
      
      def __setattr__(self,key):
        column_check=self.column_check_by_name[key]
        column_check.set(value)
      
    cls.RowCheck=RowCheck
      
        
    obj=Row.jsonToObj(doc) # instantiates and returns a new RowCheck object 
    # 
    
    
    value=obj.key1   => returns value (from RowCheck.column_check_by_name[key1].value == ColumnCheck.value)
    obj.key1=value   => perform the check => if ok, value goes into RowCheck.column_check_by_name[key1] == ColumnCheck.value
    
    
    class ColumnCheck: # internal class of each Column class
    
      def __init__(self):
        self.value=default_value
        
      def get(self):
        return self.value # always correct, of course..
        
      def set(self,value):
        # perform type and limits check here
        self.value=value
    """
      
      
  def __init__(self,**kwargs):
    self.pre=self.__class__.__name__+" : " # auxiliary string for debugging output
    parameterInitCheck(self.parameter_defs,kwargs,self) # check kwargs agains parameter_defs, attach ok'd parameters to this object as attributes
    self.initColumns()
    self.makeWidget()
    self.customInit()
    
    
  def customInit(self):
    pass
    
  
  def initColumns(self):
    # find class variables ..
    self.column_by_name=collections.OrderedDict()
    # self.columns_=[] # list of tuples: name, label, instance
    self.columns_=[] # now just a list of column instances
  
    for column_def in self.columns:
      col_instance=column_def.instantiate() # instantiate the column
      self.column_by_name[col_instance.key_name]=col_instance
      self.columns_.append(col_instance)
      
      
  def getName(self):
    """Return a name of this class that can be displayed (instead of just the classname)
    """
    if self.__class__.name:
      return self.__class__.name
    return self.__class__.__name__
    

  
  def __getattr__(self,key):
    try:
      column=self.column_by_name[key]
    except KeyError:
      raise(AttributeError("No such column "+str(key)))
      return
    else:
      return column
  
    
    
  def __getitem__(self,key):
    try:
      column=self.column_by_name[key]
    except KeyError:
      raise(AttributeError("No such column "+str(key)))
      return
    else:
      return column
    
    
  def __str__(self):
    st=""
    for key, column in self.column_by_name.items():
      st+=key+":"+str(column.getValue())+" "
    return st
  
  
  def __collect__(self):
    """Collect dictionary from QWidgets
    """
    dic={} # this will be written to db
    for key, column in self.column_by_name.items():
      dic[key]=column.getValue()
    # dic["classname"]=self.__class__.__name__ # not here, but in collection
    return dic
    
    
  def new(self,collection):
    """New entry to collection
    """
    dic=self.__collect__()
    return collection.new(self.__class__,dic)
    
  
  def update(self,collection,_id):
    """Save from QtWidgets to collection
    """
    dic=self.__collect__()
    dic["_id"]=_id
    # print(self.pre,"update",dic)
    collection.update(self.__class__,dic)
    
    
  def delete(self,collection,_id):
    """Delete a record
    """
    collection.delete(_id)
    
    
  def clear(self):
    for key, column in self.column_by_name.items():
        # print(self.pre,"clear",key)
        column.reset()
    
    
  def get(self,collection,_id):
    """Load one entry from db to QtWidgets
    """
    it =collection.get({"_id":_id}) # there should be only one ..
    try:
      res=next(it)
    except StopIteration:
      print(self.pre,"get : Could not get _id=",_id)
      return
    
    # print(self.pre,"get",res)
    
    for key, column in self.column_by_name.items():
      try:
        val=res[key]
      except KeyError:
        print(self.pre,"get : WARNING : record does not have column",key,"full record=",res)
        column.reset()
      else:
        column.setValue(val)
    
    
  def set_(self,dic):
    """Sets the widget values
    """
    for key, column in self.column_by_name.items():
      try:
        val=dic[key]
      except KeyError:
        print(self.pre,"get : WARNING : record does not have column",key,"full record=",res)
        column.reset()
      else:
        column.setValue(val)
        
        
  def set_column_value(self, col_key, value):
    """Sets the value of one column in the widget
    """
    self.column_by_name[col_key].setValue(value)
    
    
  def get_column_value(self, col_key):
    """Gets a value from one column of the widget
    """
    return self.column_by_name[col_key].getValue()
    
    
  def makeWidget(self):
    """Creates a Qt form, using the column structure
    """
    self.widget=QtWidgets.QWidget()
    self.lay   =QtWidgets.QGridLayout(self.widget)
    """
    for key in self.column_by_name:
      print(self.pre,"makeWidget: >>",key)
    """
    
    for i, column in enumerate(self.columns_):
      if (column.widget!=None):
        # labelname  =col[1]
        # column     =col[2] # the instance
        labelname    =column.label_name
        
        label=QtWidgets.QLabel(labelname,self.widget)
        column.widget.setParent(self.widget)
        # add to the layout
        self.lay.addWidget(label,        i,0)
        self.lay.addWidget(column.widget,i,1)
    
        sig = column.getNotifySignal()
        if (sig):
          sig.connect(self.update_notify_slot)
    
        # print(self.pre,"makeWidget :",labelname,label,column.widget)
    
    
  def updateWidget(self):
    """Updates the widgets.  This is necessary if columns relate to documents that have been changed.
    """
    for key, column in self.column_by_name.items():
      column.updateWidget()
    
    
  def update_notify_slot(self):
    # print(self.pre, "update_notify_slot")
    pass
    
    
  def purge(self, dic):
    if (verbose): print(self.pre,"purge",dic)
    # uses self.keyset
    needs_update=False
    tmpdic=copy.deepcopy(dic)
    tmpdic.pop("_id"); tmpdic.pop("classname") # remove metadata
    dicset=set(tmpdic)   # fields in the record to be checked
    # the document record has extra fields:
    for df in dicset.difference(self.keyset): # dicset-keyset = extra keys in dicset
      if (verbose): print(self.pre,"purge : removing key",df,"from",dic)
      dic.pop(df) # remove fields from the record
      needs_update=True
    # the document record is missing fields:
    for df in self.keyset.difference(dicset): # keyset-dicset = keyset has more keys
      dic[df]=self.column_by_name[df].getValue() # gets the default value
      if (verbose): print(self.pre,"purge : appending key/value",df,dic[df],"full record now=",dic)
      needs_update=True
    # by now the document should be consistent with the schema in self.keys
    for key in self.keys: # run through all key value pairs
      col=self.column_by_name[key]
      update, val=col.purge(dic[key]) # purge dangling foreign key references.  Return valid reference(s) in val
      if (update):
        if (verbose): print(self.pre,"purge : updated value in key",key,"to",val)
        dic[key]    =val
        needs_update=True
      
    return needs_update, dic
    
    
  
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

