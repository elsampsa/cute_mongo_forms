"""<rtf>
In this lesson, we define two different column patterns (i.e. Row classes) than can be used in the same [document database] collection.  As this is not an SQL database, rows in the same document (or "table") do not have to conform to the same column pattern (or "schema").

In the main Qt program, records in the database are presented as a Qt list, and on the right, a form with the details of the record are shown.
<rtf>"""
import sys
# from PyQt5 import QtWidgets, QtCore, QtGui # Qt5
from PySide2 import QtWidgets, QtCore, QtGui
from cute_mongo_forms.column import LineEditColumn
from cute_mongo_forms.row import ColumnSpec, Row
from cute_mongo_forms.container import List, FormSet
from cute_mongo_forms.db import SimpleCollection

"""<rtf>
Define a Row:
<rtf>"""
class PersonRow(Row):
  
  columns=[
    ColumnSpec(LineEditColumn, key_name="firstname", label_name="First Name"),
    ColumnSpec(LineEditColumn, key_name="surname",   label_name="Surname"),
    ColumnSpec(LineEditColumn, key_name="address",   label_name="Address")
  ]
  
"""<rtf>
Define another, slightly different Row:
<rtf>"""
class PersonRowExtended(Row):
  
  columns=[
    ColumnSpec(LineEditColumn, key_name="firstname", label_name="First Name"),
    ColumnSpec(LineEditColumn, key_name="secondname",label_name="Second Name"),
    ColumnSpec(LineEditColumn, key_name="surname",   label_name="Surname"),
    ColumnSpec(LineEditColumn, key_name="address",   label_name="Address")
  ]
  
  
"""<rtf>
Create collection.  SimpleCollection is a simple test database (just a python dictionary), but the interface to MongoDB works with the same API
<rtf>"""
collection=SimpleCollection(
  filename="simple_test.db",
  row_classes=[PersonRow,PersonRowExtended]
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
The Qt program.  The new part here is, that we instantiate a *FormSet*.  It uses the collection to create forms for both *PersonRow* and *PersonRowExtended* and shows the active form, depending on what the user has chosen in *PersonList*.

There is also a demo on how to manipulate the database programmatically (outside the GUI)
<rtf>"""

class MyGui(QtWidgets.QMainWindow):


  def __init__(self,parent=None):
    super(MyGui, self).__init__()
    self.initVars()
    self.setupUi()
    
    
  def initVars(self):    
    # Write a few entries to it
    collection.new(PersonRow,{"firstname":"Paavo",  "surname":"Vayrynen",  "address":"Koukkusaarentie 1"} )
    collection.new(PersonRow,{"firstname":"Martti", "surname":"Ahtisaari", "address":"Lokkisaarentie 1"}  )
    
    # Write some entries corresponding to the second row type as well
    collection.new(PersonRowExtended,{"firstname":"Juho", "secondname":"Kustaa","surname":"Paasikivi", "address":"Kontulankaari 1"})
    collection.new(PersonRowExtended,{"firstname":"Esko", "secondname":"Iiro",  "surname":"Seppänen",  "address":"Mellunraitti 3"} )
    
    # Dump the database into the terminal
    it=collection.get()
    for i in it:
      print(">>",i)


  def setupUi(self):
    self.setGeometry(QtCore.QRect(100,100,800,800))
    self.w=QtWidgets.QWidget(self)
    self.setCentralWidget(self.w)
    self.lay=QtWidgets.QHBoxLayout(self.w)
    
    # Create a list
    self.lis=PersonList(collection=collection)
    
    # Get lists's widget
    self.lis.widget.setParent(self.w)
    
    # Add to main layout
    self.lay.addWidget(self.lis.widget)
    
    # Create a group of forms
    self.formset=FormSet(collection=collection)
    
    # Get form's widget.  It encapsulates the form widgets of each row type
    self.formset.widget.setParent(self.w)
    
    # Add formset to layout
    self.lay.addWidget(self.formset.widget)
    
    # Inform formset about the item in question
    self.lis.widget.currentItemChanged.connect(self.formset.chooseForm_slot)
    
    # self.findSome() # enable this for demonstrating the "manual" (i.e. outside the GUI) manipulation of the database
    
    
  def findSome(self):
    # In this example we use SimpleCollection (just a demo database).  For MongoCollection, you would use pymongo syntax to perform queries.
    
    # (1) Search all "PersonRowExtended" rows with their secondname being "Kustaa"
    it=collection.get({"classname":"PersonRowExtended","secondname":"Kustaa"}) # Returns an iterator.
    doc=next(it) # a python dictionary
    
    # (2) Search all "PersonRowExtended" rows
    it=collection.get({"classname":"PersonRowExtended"}) # Returns an iterator.
    for doc in it:
      print(doc) # python dictionary
      
    # (3) Change values in the database programmatically and after that, update the fields in the widgets
    doc["secondname"]="Kusti"
    collection.update(PersonRowExtended,doc)
    self.lis.update()
    
    
"""<rtf>
Start the main Qt program
<rtf>"""
if (__name__=="__main__"):
  app=QtWidgets.QApplication([])
  gui=MyGui()
  gui.show()
  app.exec_()


