"""
NAME.py : Description of the file

* Copyright: 2017 [copyright holder]
* Authors  : Sampsa Riikonen
* Date     : 2017
* Version  : 0.1

This file is part of the cute_mongo_forms library

[copy-paste your license here]
"""

import sys
# import pymongo
# from PyQt5 import QtWidgets, QtCore, QtGui # Qt5
from PySide2 import QtWidgets, QtCore, QtGui
from cute_mongo_forms.tools import typeCheck, dictionaryCheck, objectCheck, parameterInitCheck, noCheck
from cute_mongo_forms.column import LineEditColumn, ComboBoxColumn, ForeignKeyColumn, CheckBoxColumn
from cute_mongo_forms.row import ColumnSpec, Row
from cute_mongo_forms.container import List, FormSet, EditFormSet, PermissionFormSet
from cute_mongo_forms.db import SimpleCollection
pre_mod = "module.submodule : " # a string for aux debuggin purposes


class TestRow(Row):
  
  columns=[
    ColumnSpec(LineEditColumn, key_name="firstname", label_name="First Name"),
    ColumnSpec(LineEditColumn, key_name="surname",   label_name="Surname"),
    ColumnSpec(LineEditColumn, key_name="address",   label_name="Address")
  ]
  
  
class TestRow1(Row):
  
  columns=[
    ColumnSpec(LineEditColumn, key_name="firstname", label_name="First Name"),
    ColumnSpec(LineEditColumn, key_name="secondname",label_name="Second Name"),
    ColumnSpec(LineEditColumn, key_name="surname",   label_name="Surname"),
    ColumnSpec(LineEditColumn, key_name="address",   label_name="Address")
  ]
  


class TestList(List):
  
  def makeLabel(self,entry):
    return entry["firstname"]+" "+entry["surname"]


 
class TestFormSet(FormSet):
  
  row_classes=[
    TestRow,
    TestRow1
    ]
  


class TestEditFormSet(EditFormSet):
  
  row_classes=[
    TestRow,
    TestRow1
    ]




class MyGui(QtWidgets.QMainWindow):

  debug=False
  # debug=True

  def __init__(self,parent=None):
    super(MyGui, self).__init__()
    self.initVars()
    self.setupUi()
    

  def initVars(self):
    pass


  def setupUi(self):
    self.setGeometry(QtCore.QRect(100,100,800,800))
    self.w=QtWidgets.QWidget(self)
    self.setCentralWidget(self.w)
    # self.lay=QtWidgets.QGridLayout(self.w)
    self.lay=QtWidgets.QHBoxLayout(self.w)
    


class TestGui1(MyGui):
  
  
  def initVars(self):
    self.collection=SimpleCollection(filename="simple_test.db")
    it=self.collection.get()
    for i in it:
      print(">>",i)
    
    
  def setupUi(self):
    super().setupUi()
    # self.row=TestRow()
    self.row=TestRow1()
    self.row.widget.setParent(self.w)
    self.lay.addWidget(self.row.widget)
    
      
  def closeEvent(self,e):
    print("close event!")
    self.row.new(self.collection)
    self.collection.close()
    e.accept()
    


class TestGui2(MyGui):

  
  def initVars(self):
    self.collection=SimpleCollection(filename="simple_test.db")
    it=self.collection.get()
    for i in it:
      print(">>",i)
    
    
  def setupUi(self):
    super().setupUi()
    self.lis=TestList(collection=self.collection)
    self.lis.widget.setParent(self.w)
    self.lay.addWidget(self.lis.widget)
    
      
  def closeEvent(self,e):
    print("close event!")
    self.collection.close()
    e.accept()
    
    
    
class TestGui3(MyGui):
  
  
  def initVars(self):
    self.collection=SimpleCollection(filename="simple_test.db")
    it=self.collection.get()
    for i in it:
      print(">>",i)
    
    
  def setupUi(self):
    super().setupUi()
    
    self.lis=TestList(collection=self.collection)
    self.lis.widget.setParent(self.w)
    self.lay.addWidget(self.lis.widget)
    
    self.formset=TestFormSet(collection=self.collection)
    self.formset.widget.setParent(self.w)
    self.lay.addWidget(self.formset.widget)
    
    self.lis.widget.     currentItemChanged.connect(self.formset.chooseForm_slot) # inform formset about the item in question
    # self.formset.signals.new_record.        connect(self.lis.update_slot)         # inform list that a new entry has been added
      
      
  def closeEvent(self,e):
    print("close event!")
    self.collection.close()
    e.accept()
  
  
  
class TestGui4(MyGui):
  
  
  def initVars(self):
    self.collection=SimpleCollection(filename="simple_test.db")
    it=self.collection.get()
    for i in it:
      print(">>",i)
    
    
  def setupUi(self):
    super().setupUi()
    
    self.lis=TestList(collection=self.collection)
    self.lis.widget.setParent(self.w)
    self.lay.addWidget(self.lis.widget)
    
    self.formset=TestEditFormSet(collection=self.collection)
    self.formset.widget.setParent(self.w)
    self.lay.addWidget(self.formset.widget)
    
    self.lis.widget.     currentItemChanged.connect(self.formset.chooseForm_slot) # inform formset about the item in question
    self.formset.signals.new_record.        connect(self.lis.update_slot)         # inform list that a new entry has been added
      
      
  def closeEvent(self,e):
    print("close event!")
    self.collection.close()
    e.accept()
    
    
    
class TestGui5(MyGui):
  """Left: list of records.  Right: details of the records, editable.  Records have a reference to a list of accepted car manufacturers
  """
  # LineEditColumn(field_name="firstname",label_name="First Name", ..)
  # ComboBoxColum(collection=.., key_column_name=..,field_name=..,label_name="Car model")
  
  
  def initVars(self):
    self.collection=SimpleCollection(filename="simple_test.db")
    it=self.collection.get()
    for i in it:
      print(">>",i)
    
    self.side_collection=SimpleCollection(filename="simple_side.db")
    self.side_collection.clear()
    self.side_collection.new({"label":"Ford"})
    self.side_collection.new({"label":"Audi"})
    
    
  def setupUi(self):
    super().setupUi()
    
    # we need self.side_collection, hence the definitions here
    class TestRow_(Row):
      columns=[
        ColumnSpec(LineEditColumn, key_name="firstname", label_name="First Name"),
        ColumnSpec(LineEditColumn, key_name="secondname",label_name="Second Name"),
        ColumnSpec(LineEditColumn, key_name="surname",   label_name="Surname"),
        ColumnSpec(ComboBoxColumn, key_name="address",   label_name="Address", collection=self.side_collection)
      ]
      
      
    class TestList_(List):
      def makeLabel(self,entry):
        return entry["firstname"]+" "+entry["surname"]

    class TestFormSet_(FormSet):  
      row_classes=[
        TestRow,
        TestRow_,
        ]
  
    class TestEditFormSet_(EditFormSet):
      row_classes=[
        TestRow,
        TestRow_
        ]
        
    
    self.lis=TestList_(collection=self.collection)
    self.lis.widget.setParent(self.w)
    self.lay.addWidget(self.lis.widget)
    
    self.formset=TestEditFormSet_(collection=self.collection)
    self.formset.widget.setParent(self.w)
    self.lay.addWidget(self.formset.widget)
    
    self.lis.widget.     currentItemChanged.connect(self.formset.chooseForm_slot) # inform formset about the item in question
    self.formset.signals.new_record.        connect(self.lis.update_slot)         # inform list that a new entry has been added
      
      
  def closeEvent(self,e):
    print("close event!")
    self.collection.close()
    e.accept()
  
  
class TestGui6(MyGui):
  """Left: list of records (users).  Right: list of cards.  Rightmost: user rights.
  """
  # LineEditColumn(field_name="firstname",label_name="First Name", ..)
  # ComboBoxColum(collection=.., key_column_name=..,field_name=..,label_name="Car model")
  
  
  def initVars(self):
    # users
    self.collection1=SimpleCollection(filename="simple_test6a.db")
    self.collection1.clear()
    
    # cars
    self.collection2=SimpleCollection(filename="simple_test6b.db")
    self.collection2.clear()
    
    # permissions
    self.collection3=SimpleCollection(filename="simple_test6c.db")
    self.collection3.clear()
    
    
  def setupUi(self):
    super().setupUi()
    
    # we need self.side_collection, hence the definitions here
    class Row1(Row):
      columns=[
        ColumnSpec(LineEditColumn, key_name="name",   label_name="First Name"),
        ColumnSpec(LineEditColumn, key_name="surname",label_name="Last Name")
      ]
    
    class Row2(Row):
      columns=[
        ColumnSpec(LineEditColumn, key_name="brand",label_name="Brand"),
        ColumnSpec(LineEditColumn, key_name="year", label_name="Year")
      ]
    
    class LinkRow(Row):
      columns=[
        ColumnSpec(ForeignKeyColumn, key_name="user_key"),
        ColumnSpec(ForeignKeyColumn, key_name="car_key"),
        ColumnSpec(CheckBoxColumn,   key_name="drive", label_name="Can drive"),
        ColumnSpec(CheckBoxColumn,   key_name="sell",  label_name="Can sell")
        ]
        
  
    class TestList1(List):
      def makeLabel(self,entry):
        return entry["name"]+" "+entry["surname"]


    class TestList2(List):
      def makeLabel(self,entry):
        return entry["brand"]


    class TestFormSet1(FormSet):  
      row_classes=[
        Row1
        ]
  
    class TestFormSet2(FormSet):  
      row_classes=[
        Row2
        ]
      
    class TestFormSet3(PermissionFormSet):
      row_classes=[
        LinkRow
        ]
      
      
    self.collection1.new(Row1,{"name":"Antti","surname":"Mykkanen"})
    self.collection1.new(Row1,{"name":"Jonne","surname":"Paananen"})
    self.collection1.new(Row1,{"name":"Juho", "surname":"Kokkonen"})
    self.collection1.new(Row1,{"name":"Janne","surname":"Suhonen" })
    
    self.collection2.new(Row2,{"brand":"Ford","year":2000})
    self.collection2.new(Row2,{"brand":"Audi","year":1996})
    self.collection2.new(Row2,{"brand":"Seat","year":2004})
    self.collection2.new(Row2,{"brand":"Yugo","year":1985})
    self.collection2.new(Row2,{"brand":"BMW", "year":2016})
        
    self.lis1=TestList1(collection=self.collection1)
    self.lis1.widget.setParent(self.w)
    self.lay.addWidget(self.lis1.widget)
    
    self.formset1=TestFormSet1(collection=self.collection1)
    self.formset1.widget.setParent(self.w)
    self.lay.addWidget(self.formset1.widget)
    
    self.lis2=TestList2(collection=self.collection2)
    self.lis2.widget.setParent(self.w)
    self.lay.addWidget(self.lis2.widget)
    
    self.formset2=TestFormSet2(collection=self.collection2)
    self.formset2.widget.setParent(self.w)
    self.lay.addWidget(self.formset2.widget)
  
    self.formset3=TestFormSet3(collection=self.collection3, key1_name="user_key", key2_name="car_key")
    self.formset3.widget.setParent(self.w)
    self.lay.addWidget(self.formset3.widget)
  
    
    self.lis1.widget.     currentItemChanged.connect(self.formset1.chooseForm_slot) # inform formset about the item in question
    self.lis2.widget.     currentItemChanged.connect(self.formset2.chooseForm_slot) # inform formset about the item in question
    
    # connect the user/car pair to the permission form
    self.lis1.widget.     currentItemChanged.connect(self.formset3.pingCol1_slot) # inform formset about the item in question
    self.lis2.widget.     currentItemChanged.connect(self.formset3.pingCol2_slot) # inform formset about the item in question
    
    
    
    # self.formset1.signals.new_record.        connect(self.lis1.update_slot)         # inform list that a new entry has been added
      
      
  def closeEvent(self,e):
    print("close event!")
    self.collection1.close()
    self.collection2.close()
    e.accept()
    
  
  
  
def main(i):
  app=QtWidgets.QApplication(["test_app_"+str(i)])
  st="mg=TestGui"+str(i)+"()"
  exec(st,globals())
  mg.show()
  app.exec_()


if (__name__=="__main__"):
  main(sys.argv[1])

