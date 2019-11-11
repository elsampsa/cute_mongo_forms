"""<rtf>
In this lesson, a collection of records is presented as a Qt list on the left and a form corresponding to an individual record is on the right, while user can interact with the form, create new entries, delete old ones and modify the existing ones.

For persons of a certain type ("PersonRowExtended"), we can mark up their favorite foods from a list.  This is achieved with ListEditColumn (see below) that creates a relation from rows of type "PersonRowExtended" to the document collection listing different kinds of foods ("food_collection").
<rtf>"""
import sys
# from PyQt5 import QtWidgets, QtCore, QtGui # Qt5
from PySide2 import QtWidgets, QtCore, QtGui
from cute_mongo_forms.column import LineEditColumn, ListEditColumn, CheckBoxColumn
from cute_mongo_forms.row import ColumnSpec, Row
from cute_mongo_forms.container import List, FormSet, EditFormSet
from cute_mongo_forms.db import SimpleCollection


"""<rtf>
Databases, Row types, containers (FormSets, etc.) are all encapsulated into a single class that describes the data model
<rtf>"""
class DataModel:
  
  
  def __init__(self):
    self.define()
    self.initDB()
  
  def define(self):
    """Define column patterns and databases
    """
    class FoodRow(Row):
      columns=[
        ColumnSpec(LineEditColumn, key_name="name", label_name="Name"),
        ColumnSpec(LineEditColumn, key_name="price",label_name="Price"),
        ColumnSpec(CheckBoxColumn, key_name="spicy",label_name="Is spicy")
      ]
    self.FoodRow=FoodRow
    
    self.food_collection =SimpleCollection(filename="food_test.db",row_classes=[self.FoodRow])
  
    class PersonRow(Row):
      columns=[
        ColumnSpec(LineEditColumn, key_name="firstname", label_name="First Name"),
        ColumnSpec(LineEditColumn, key_name="surname",   label_name="Surname"),
        ColumnSpec(LineEditColumn, key_name="address",   label_name="Address"),
        ColumnSpec(CheckBoxColumn, key_name="married",   label_name="Is married")
      ]
    self.PersonRow=PersonRow
      
    class PersonRowExtended(Row):
      columns=[
        ColumnSpec(LineEditColumn, key_name="firstname", label_name="First Name"),
        ColumnSpec(LineEditColumn, key_name="secondname",label_name="Second Name"),
        ColumnSpec(LineEditColumn, key_name="surname",   label_name="Surname"),
        ColumnSpec(LineEditColumn, key_name="address",   label_name="Address"),
        # in the following, we're referring to self.food_collection and there, to the columns with keys "_id" and "name".  The ListEditColumn itself is a list of foreign_keys
        ColumnSpec(ListEditColumn, key_name="foods",     label_name="Favorite foods",  collection=self.food_collection, foreign_label_name="name")
      ]
    self.PersonRowExtended=PersonRowExtended
      
    self.collection =SimpleCollection(filename="simple_test.db",row_classes=[PersonRow,PersonRowExtended])
      
    class PersonList(List):
      def makeLabel(self,entry):
        try:
          st=entry["firstname"]+" "+entry["surname"]
        except KeyError:
          st="?"
        return st
    self.PersonList=PersonList
      
      
  def initDB(self):
    """Write some entries to databases
    """    
    self.collection.new(self.PersonRow,{"firstname":"Paavo",  "surname":"Vayrynen",  "address":"Koukkusaarentie 1", "married":True} )
    self.collection.new(self.PersonRow,{"firstname":"Martti", "surname":"Ahtisaari", "address":"Lokkisaarentie 1",  "married":True} )
    
    # add some foods
    self.food_collection.new(self.FoodRow,{"name":"Hamburger","price":10, "spicy":False})
    self.food_collection.new(self.FoodRow,{"name":"Hotdog",   "price":50, "spicy":False})
    self.food_collection.new(self.FoodRow,{"name":"Freedom Fries",   "price":10, "spicy":False})
    self.food_collection.new(self.FoodRow,{"name":"Bacalao",   "price":100,"spicy":False})
    self.food_collection.new(self.FoodRow,{"name":"Piparra",   "price":1,  "spicy":True})
    
    # get ids of some foods ..
    bacalao=list(self.food_collection.get(query={"name":"Bacalao"}))[0]["_id"]
    piparra=list(self.food_collection.get(query={"name":"Piparra"}))[0]["_id"]
    
    self.collection.new(self.PersonRowExtended,{"firstname":"Juho", "secondname":"Kustaa","surname":"Paasikivi", "address":"Kontulankaari 1", "foods":[] })
    self.collection.new(self.PersonRowExtended,{"firstname":"Esko", "secondname":"Iiro",  "surname":"Seppänen",  "address":"Mellunraitti 3",  "foods":[bacalao, piparra] })
    
  
"""<rtf>
The main Qt program
<rtf>"""
class MyGui(QtWidgets.QMainWindow):


  def __init__(self,parent=None):
    super(MyGui, self).__init__()
    self.initVars()
    self.setupUi()
    
    
  def initVars(self):
    # Connect to db, define column patters (i.e. rows), 
    self.data_model=DataModel()
    
    
  def setupUi(self):
    self.setGeometry(QtCore.QRect(100,100,800,800))
    self.w=QtWidgets.QWidget(self)
    self.setCentralWidget(self.w)
    self.lay=QtWidgets.QHBoxLayout(self.w)
    
    # Create a list
    self.lis=self.data_model.PersonList(collection=self.data_model.collection)
    
    # Get lists's widget
    self.lis.widget.setParent(self.w)
    
    # Add to main layout
    self.lay.addWidget(self.lis.widget)
    
    # Create a group of forms
    self.formset=EditFormSet(collection=self.data_model.collection)
    
    # Get form's widget and set it's parent to the current main widget
    self.formset.widget.setParent(self.w)
    
    # Add formset to layout
    self.lay.addWidget(self.formset.widget)
    
    # Inform formset about the item in question.  "self.lis.widget" is a QListWidget instance.
    self.lis.widget.currentItemChanged. connect(self.formset.chooseForm_slot)
    
    # inform list when a new record has been added or when a record has been saved
    self.formset.signals.new_record.    connect(self.lis.update_slot)
    self.formset.signals.save_record.   connect(self.lis.update_slot)

"""<rtf>
Start the Qt program
<rtf>"""
if (__name__=="__main__"):
  app=QtWidgets.QApplication([])
  gui=MyGui()
  gui.show()
  app.exec_()

 
