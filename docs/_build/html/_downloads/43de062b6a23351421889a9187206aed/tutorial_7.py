"""<rtf>
This is like lesson 6, but now the user can simultaneously edit the person and food document collections.  If a food is erased from the collection, it also disappears from the food list in the person collection, i.e. there is an automatic update for forms that depend through relations on other document collections.
<rtf>"""
import sys
# from PyQt5 import QtWidgets, QtCore, QtGui # Qt5
from PySide2 import QtWidgets, QtCore, QtGui
from cute_mongo_forms.column import LineEditColumn, ListEditColumn, CheckBoxColumn
from cute_mongo_forms.row import ColumnSpec, Row
from cute_mongo_forms.container import List, FormSet, EditFormSet
from cute_mongo_forms.db import SimpleCollection

"""<rtf>
This class helps us to group lists and forms together
<rtf>"""
class ListAndForm:
  
  def __init__(self,lis,form,title="",parent=None):
    self.title=title
    self.lis  =lis
    self.form =form
    
    self.widget =QtWidgets.QWidget(parent) # create a new widget
    self.lay    =QtWidgets.QVBoxLayout(self.widget) # attach layout to that widget
    self.label  =QtWidgets.QLabel(self.title,self.widget)
    
    self.subwidget=QtWidgets.QWidget(self.widget)
    self.sublay   =QtWidgets.QHBoxLayout(self.subwidget)
    
    self.lay.addWidget(self.label)
    self.lay.addWidget(self.subwidget)
    
    self.lis. widget.setParent(self.subwidget) # get widget from List and set its parent to widget
    self.form.widget.setParent(self.subwidget)
    self.sublay. addWidget(self.lis.widget) # add List's internal widget to widget's layout
    self.sublay. addWidget(self.form.widget)
    self.lis.widget.currentItemChanged. connect(self.form.chooseForm_slot) # connections between list and the form
    self.form.signals.new_record.       connect(self.lis.update_slot)
    self.form.signals.save_record.      connect(self.lis.update_slot)
    self.form.signals.delete_record.    connect(self.lis.update_slot)

    self.delete   =self.form.signals.delete_record # shorthand
    self.modified =self.form.signals.modified


  def update(self):
    self.form.updateWidget()
    

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

    class FoodList(List):
      def makeLabel(self,entry):
        try:
          st=entry["name"]+" ("+str(entry["price"])+" EUR)"
        except KeyError:
          st="?"
        return st
    self.FoodList=FoodList
      
      
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
    
    self.person_view=ListAndForm(self.data_model.PersonList(collection=self.data_model.collection),     EditFormSet(collection=self.data_model.collection),     "Persons",self.w)
    self.food_view  =ListAndForm(self.data_model.FoodList(collection=self.data_model.food_collection),  EditFormSet(collection=self.data_model.food_collection),"Foods",  self.w)
    
    self.food_view.modified.connect(self.person_view.update)
    
    # instantiate PersonFormSet => instantiate rows => row instantiates widgets based on the columns => ..
    # updating: call row's updateWidget method => re-creates column widgets
    
    self.lay.addWidget(self.person_view.widget)
    self.lay.addWidget(self.food_view.widget)
    
    
"""<rtf>
Start the Qt program
<rtf>"""
if (__name__=="__main__"):
  app=QtWidgets.QApplication([])
  gui=MyGui()
  gui.show()
  app.exec_()


