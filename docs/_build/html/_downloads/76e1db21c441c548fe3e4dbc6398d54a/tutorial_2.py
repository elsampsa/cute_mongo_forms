"""<rtf>
In this lesson, we create a database, write a few entries to it, and see the database contents in a Qt list.
<rtf>"""
import sys
# from PyQt5 import QtWidgets, QtCore, QtGui # Qt5
from PySide2 import QtWidgets, QtCore, QtGui
from cute_mongo_forms.column import LineEditColumn
from cute_mongo_forms.row import ColumnSpec, Row
from cute_mongo_forms.container import List
from cute_mongo_forms.db import SimpleCollection


"""<rtf>
Define a Row, i.e. a pattern of columns
<rtf>"""
class PersonRow(Row):
  
  columns=[
    ColumnSpec(LineEditColumn, key_name="firstname", label_name="First Name"),
    ColumnSpec(LineEditColumn, key_name="surname",   label_name="Surname"),
    ColumnSpec(LineEditColumn, key_name="address",   label_name="Address")
  ]

"""<rtf>
Define the collection
<rtf>"""  
collection=SimpleCollection(
  filename="simple_test.db",
  row_classes=[PersonRow]
  )
  

"""<rtf>
Next we create a list of database entries.  The List class is Row agnostic.  It only knows how to create a label, using a Row entry.  The only method we need to overwrite is the one used to create a label:
<rtf>"""
class PersonList(List):
  
  def makeLabel(self,entry):
    try:
      st=entry["firstname"]+" "+entry["surname"]
    except KeyError:
      st="?"
    return st


"""<rtf>
Here comes the Qt program.  At the **initVars** method, create a database, add some entries to the database and dump the database to the terminal.
  
SimpleCollection is a simple test database (just a python dictionary), but the interface to MongoDB works with the same API
<rtf>"""

class MyGui(QtWidgets.QMainWindow):


  def __init__(self,parent=None):
    super(MyGui, self).__init__()
    self.initVars()
    self.setupUi()
    
    
  def initVars(self):
    # Write a few entries to the collection
    collection.new(PersonRow,{"firstname":"Paavo",  "surname":"Vayrynen",  "address":"Koukkusaarentie 1"} )
    collection.new(PersonRow,{"firstname":"Martti", "surname":"Ahtisaari", "address":"Lokkisaarentie 1"}  )
    
    # Dump the database
    it=collection.get()
    for i in it:
      print(">>",i)


  def setupUi(self):
    self.setGeometry(QtCore.QRect(100,100,800,800))
    self.w=QtWidgets.QWidget(self)
    self.setCentralWidget(self.w)
    self.lay=QtWidgets.QHBoxLayout(self.w)
    
    # Create a list view of a collection.  We need to provide a collection, of course
    self.lis=PersonList(collection=collection)
    
    # Get lists's widget, set its parent to the current main widget
    self.lis.widget.setParent(self.w)
    
    # Add to main layout
    self.lay.addWidget(self.lis.widget)
    

"""<rtf>
Start the main Qt program
<rtf>"""
if (__name__=="__main__"):
  app=QtWidgets.QApplication([])
  gui=MyGui()
  gui.show()
  app.exec_()
   

