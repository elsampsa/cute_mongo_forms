"""
mongo.py   : Database interface for MongoDB

* Copyright: 2017-2018 Sampsa Riikonen
* Authors  : Sampsa Riikonen
* Date     : 2018
* Version  : 0.1

This file is part of the cute_mongo_forms library

License: LGPLv3+ (see the COPYING.LESSER file)
"""

import sys
from cute_mongo_forms.tools import typeCheck, dictionaryCheck, objectCheck, parameterInitCheck, noCheck
from cute_mongo_forms.db.base import Collection
import pymongo
pre_mod = "db.mongo : " # a string for aux debugging purposes
verbose=False # module's verbosity


class MongoCollection(Collection):
  """Let's do Mongo!
  """
  
  parameter_defs={
    "database_name"   : str,
    "collection_name" : str,
    "row_classes"     : list
    }

  
  def __init__(self,**kwargs):
    self.pre=self.__class__.__name__+" : " # auxiliary string for debugging output
    parameterInitCheck(self.parameter_defs,kwargs,self) # check kwargs agains parameter_defs, attach ok'd parameters to this object as attributes
    self.client    =pymongo.MongoClient()
    self.db        =self.client[self.database_name]
    self.collection=self.db[self.collection_name]
    
    
  def removeDB(self):
    # extra method for mongo
    self.db.remove()
    
    
  def clear(self):
    self.collection.remove()
    self.collection=self.db[self.collection_name]
    
    
  def save(self):
    # no explicit save needed..
    pass
    
    
  def close(self):
    self.client.close()
    
    
  def new(self,cls,dic):
    super().new(cls,dic)
    if (verbose): print(self.pre,"new :",dic)
    dic["classname"]=cls.__name__    
    result=self.collection.insert_one(dic)
    return result.inserted_id
    
    
  def update(self,cls,dic):
    """Substitute element from list with same "_id"
    """
    if (verbose): print(self.pre,"update :",dic)
    super().update(cls,dic)
    _id=dic.pop("_id")
    dic["classname"]=cls.__name__
    result=self.collection.replace_one({"_id":_id},dic)
    if (result.matched_count<1):
      print(self.pre,"update: could not update",dic)
    
      
  def delete(self,_id):
    result=self.collection.delete_one({"_id":_id})
    if (result.deleted_count<1):
      print(self.pre,"update: could not delete",dic)
      
    
  def get(self,query={}):
    """Returns an iterator that has matched elements
    """
    if (verbose): print(self.pre,"get : query=",query)
    return self.collection.find(query)
    
  
  def __str__(self):
    st="\n-------------\n"
    for l in self.get():
      st+=str(l)+"\n"
    st+="\n-------------\n"  
    return st
  
  
    
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

