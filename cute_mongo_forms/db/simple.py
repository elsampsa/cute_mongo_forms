"""
simple.py  : A simple test database where the document collection is just a python list

* Copyright: 2017-2018 Sampsa Riikonen
* Authors  : Sampsa Riikonen
* Date     : 2017
* Version  : 0.1

This file is part of the cute_mongo_forms library

License: LGPLv3+ (see the COPYING.LESSER file)
"""

import sys
import copy
import os
# import pickle
import json
import time
from cute_mongo_forms.tools import typeCheck, dictionaryCheck, objectCheck, parameterInitCheck, noCheck
from cute_mongo_forms.db.base import Collection
pre_mod = "db.simple : " # a string for aux debugging purposes


class SimpleCollection(Collection):
  """A "mock" document collection.  The document in this "database" is just a python list that's saved on the disk.  This might even work if your document database is small (say, less than ~ 10 000 docs).
  """
  
  parameter_defs={
    "filename"     : (str,"simple_collection.db"),
    "row_classes"  : list
    }

  
  def __init__(self,**kwargs):
    self.pre=self.__class__.__name__+" : " # auxiliary string for debugging output
    parameterInitCheck(self.parameter_defs,kwargs,self) # check kwargs agains parameter_defs, attach ok'd parameters to this object as attributes
    if (os.path.exists(self.filename)):
        """
        f=open(self.filename,"br")
        self.lis=pickle.load(f)
        # print(self.pre,"loaded",self.lis)
        f.close()
        """
        f=open(self.filename,"r")
        self.lis=json.loads(f.read())
        f.close()
    else:
        self.clear()

    
  def clear(self):
    self.lis=[] # All data of this "database" is here. :)
    
    
  def save(self):
    """
    f=open(self.filename,"bw")
    pickle.dump(self.lis,f)
    f.close()
    """
    f=open(self.filename,"w")
    f.write(json.dumps(self.lis))
    f.close()
    
    
  def close(self):
    self.save()
    
    
  def new(self,cls,dic):
    super().new(cls,dic)
    dic["_id"]      =int(time.time()*1000000) # microsecond timestamp
    dic["classname"]=cls.__name__
    self.lis.append(dic)
    return dic["_id"]
    
    
  def update(self,cls,dic):
    """Substitute element from list with same "_id"
    """
    super().update(cls,dic)
    l_=None
    for l in self.lis:
      if (dic["_id"]==l["_id"]):
        l_=l
        
    if (l_==None):
      print("could not update",dic)
    else:
      dic["classname"]=cls.__name__
      self.lis.remove(l_)
      self.lis.append(dic)
      
      
  def delete(self,_id):
    els=[]
    els=list(self.get(query={"_id":_id}))
    for el in els:
      self.lis.remove(el)
    
  
  def get(self,query={}):
    """Returns an iterator that has matched elements
    """
    for l in copy.deepcopy(self.lis):
      ok=True
      for key in query:
        if ((key in l) and (query[key]==l[key])):
          pass
        else:
          ok=False
      if ok:
        yield l
    
  
  def __str__(self):
    st="-------------\n"
    for l in self.lis:
      st+=str(l)+"\n"
    st+="-------------\n"  
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

