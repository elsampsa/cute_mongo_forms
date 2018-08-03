"""<rtf>
In this lesson we use a simple relation.

We create a user rights scheme for persons wishing to use some resources - cars in this case.  The collection schema looks like this:

::

       person_collection           link_collection            car_collection
    +--------------------+      +------------------+      +--------------------+
    |  _id               |<-+   |  _id             |   +->| _id                |
    |  name              |  +---|  user_key        |   |  | brand              |
    |  surname           |      |  car_key         |---+  | year               | 
    |                    |      |  drive           |      |                    |
    |                    |      |  sell            |      |                    |
    +--------------------+      +------------------+      +--------------------+

An entry in the link_collection gives a person the right to use a certain car.

In the user interface, user can choose a person and a car and grant user rights by pressing the "NEW" button on the right.
<rtf>"""
import sys
# from PyQt5 import QtWidgets, QtCore, QtGui # Qt5
from PySide2 import QtWidgets, QtCore, QtGui
from cute_mongo_forms.column import LineEditColumn, ComboBoxColumn, ForeignKeyColumn, CheckBoxColumn
from cute_mongo_forms.row import ColumnSpec, Row
from cute_mongo_forms.container import List, FormSet, EditFormSet, PermissionFormSet
from cute_mongo_forms.db import SimpleCollection
    

"""<rtf>
Create the column patters (Rows) for each collection.
<rtf>"""
class PersonRow(Row):
  columns=[
    ColumnSpec(LineEditColumn, key_name="name",   label_name="First Name"),
    ColumnSpec(LineEditColumn, key_name="surname",label_name="Last Name")
  ]

person_collection=SimpleCollection(
  filename="persons.db",
  row_classes=[PersonRow]
  )
person_collection.clear()

  
class CarRow(Row):
  columns=[
    ColumnSpec(LineEditColumn, key_name="brand",label_name="Brand"),
    ColumnSpec(LineEditColumn, key_name="year", label_name="Year")
  ]
  
car_collection=SimpleCollection(
  filename="cars.db",
  row_classes=[CarRow]
  )
car_collection.clear()
  

"""<rtf>
Here we are referencing to foreign keys.  The *ForeignKeyColumn* column type is a special column that's not visualized in the form widget ("label_name" is missing).  It's only used for referencing records in other collections:
<rtf>"""
class LinkRow(Row):
  columns=[
    ColumnSpec(ForeignKeyColumn, key_name="user_key", collection=person_collection),
    ColumnSpec(ForeignKeyColumn, key_name="car_key",  collection=car_collection),
    ColumnSpec(CheckBoxColumn,   key_name="drive", label_name="Can drive"),
    ColumnSpec(CheckBoxColumn,   key_name="sell",  label_name="Can sell")
  ]
    
link_collection=SimpleCollection(
  filename="links.db",
  row_classes=[LinkRow]
  )
link_collection.clear()

  
"""<rtf>
Create lists and forms for each collection.

In Lists, just define how a record is visualized in the list.
<rtf>"""
class PersonList(List):
  def makeLabel(self,entry):
    try:
      return entry["name"]+" "+entry["surname"]
    except KeyError:
      return "?"


class CarList(List):
  def makeLabel(self,entry):
    try:
      return entry["brand"]
    except KeyError:
      return "?"


"""<rtf>
The main Qt program.  PermissionFormSet is a special FormSet class for handling rights through link tables.
<rtf>"""
class MyGui(QtWidgets.QMainWindow):


  def __init__(self,parent=None):
    super(MyGui, self).__init__()
    self.initVars()
    self.setupUi()
    
    
  def initVars(self):
    # add persons to the collection
    person_collection.new(PersonRow,{"name":"Antti","surname":"Mykkanen"})
    person_collection.new(PersonRow,{"name":"Jonne","surname":"Paananen"})
    person_collection.new(PersonRow,{"name":"Juho", "surname":"Kokkonen"})
    person_collection.new(PersonRow,{"name":"Janne","surname":"Suhonen" })
    
    # add cars to the collection
    car_collection.new(CarRow,{"brand":"Ford","year":2000})
    car_collection.new(CarRow,{"brand":"Audi","year":1996})
    car_collection.new(CarRow,{"brand":"Seat","year":2004})
    car_collection.new(CarRow,{"brand":"Yugo","year":1985})
    car_collection.new(CarRow,{"brand":"BMW", "year":2016})


  def setupUi(self):
    # self.setGeometry(QtCore.QRect(100,100,800,800))
    self.w=QtWidgets.QWidget(self)
    self.setCentralWidget(self.w)
    self.lay=QtWidgets.QHBoxLayout(self.w)
    
    # List view of person_collection
    self.person_lis=PersonList(collection=person_collection)
    self.person_lis.widget.setParent(self.w)
    self.lay.addWidget(self.person_lis.widget)
    
    # Form views of individual records in the person_collection
    self.person_form=FormSet(collection=person_collection)
    self.person_form.widget.setParent(self.w)
    self.lay.addWidget(self.person_form.widget)
    
    # List view of car_collection
    self.car_lis=CarList(collection=car_collection)
    self.car_lis.widget.setParent(self.w)
    self.lay.addWidget(self.car_lis.widget)
    
    # Form view of records in car_collection
    self.car_form=FormSet(collection=car_collection)
    self.car_form.widget.setParent(self.w)
    self.lay.addWidget(self.car_form.widget)
  
    # Form view of the Link table
    self.permission_form=PermissionFormSet(collection=link_collection, key1_name="user_key", key2_name="car_key")
    self.permission_form.widget.setParent(self.w)
    self.lay.addWidget(self.permission_form.widget)
  
    # Create connections between list views, forms, etc.
    self.person_lis.widget. currentItemChanged. connect(self.person_form.chooseForm_slot) # inform person formset about the item in question
    self.car_lis.widget.    currentItemChanged. connect(self.car_form.   chooseForm_slot) # inform car formset about the item in question
    
    # Connect the user/car pair to the permission form
    self.person_lis.widget. currentItemChanged. connect(self.permission_form.chooseRecord1_slot) # inform formset about the item in question
    self.car_lis.widget.    currentItemChanged. connect(self.permission_form.chooseRecord2_slot) # inform formset about the item in question
    
    
"""<rtf>
Start the main Qt program
<rtf>"""
if (__name__=="__main__"):
  app=QtWidgets.QApplication([])
  gui=MyGui()
  gui.show()
  app.exec_()

