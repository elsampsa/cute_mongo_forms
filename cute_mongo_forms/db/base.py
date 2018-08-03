"""
base.py    : Database base classes

* Copyright: 2017-2018 Sampsa Riikonen
* Authors  : Sampsa Riikonen
* Date     : 2018
* Version  : 0.1

This file is part of the cute_mongo_forms library

License: LGPLv3+ (see the COPYING.LESSER file)
"""

import sys
from cute_mongo_forms.tools import typeCheck, dictionaryCheck, objectCheck, parameterInitCheck, noCheck
from cute_mongo_forms.row.base import RowWatcher
pre_mod = "db.base : " # a string for aux debuggin purposes
verbose=False # module's verbosity
# verbose=True

class Collection:
  
  parameter_defs={
    "row_classes" : list
    }
  
  
  def __init__(self,**kwargs):
    self.pre=self.__class__.__name__+" : " # auxiliary string for debugging output
    parameterInitCheck(self.parameter_defs,kwargs,self) # check kwargs agains parameter_defs, attach ok'd parameters to this object as attributes


  def getRowClasses(self):
    return self.row_classes
  
  
  def new(self,cls,dic):
    """New entry.  A class instance (cls) is required (base class: Row)
    """
    # TODO: check that cls is actually at self.row_classes..!
    assert(type(cls)==RowWatcher)
    assert(type(dic)==dict)
    if (set(cls.keys)==set(dic)):
      pass
    else:
      raise AssertionError("Class columns="+str(cls.keys)+" not equal to keys="+str(dic.keys()))
    
    
  def update(self,cls,dic):
    """Substitute element from list with same "_id"
    """
    assert(type(cls)==RowWatcher)
    assert(type(dic)==dict)
    assert("_id" in dic)
    

  def delete(self,_id):
    """Delete an element corresponding to _id
    """
    pass
    

  def get(self,query={}):
    """Returns an iterator that matches the search
    """
    return iter([])


  def close(self):
    """What to do at exit?
    """
    self.save()

  
  def save(self):
    """Save the state of the database (for mongo, leave this empty)
    """
    pass
  
  
  def purge(self):
    """Purge the collection of erroneous records, add/remove keys if necessary and remove "dangling" references to foreign keys
    """
    if (verbose): print(self.pre,"purge")
    self.row_instance_by_name={}
    for row_class in self.row_classes:
      self.row_instance_by_name[row_class.__name__]=row_class() # each row has a widget attribute which is the root of the column qt widgets
    
    for dic in self.get():
      if (verbose): print("\n",self.pre,"purge : dic=",dic)
      if ("classname" not in dic): # no "classname" .. can't instantiate a class.  Remove this record
        self.delete(dic["_id"])
      elif (dic["classname"] not in self.row_instance_by_name): # no such class  .. Remove
        self.delete(dic["_id"])
      else:
        needs_update=False # by default, no update is needed
        classname=dic["classname"]
        row=self.row_instance_by_name[classname]
        needs_update, newdic =row.purge(dic)
        if (needs_update):
          self.update(row.__class__,dic)
      

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

