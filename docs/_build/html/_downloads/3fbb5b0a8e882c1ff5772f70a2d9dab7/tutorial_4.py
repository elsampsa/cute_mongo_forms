"""<rtf>
In this lesson, a collection of records is presented as a Qt list on the left and a form corresponding to an individual record is on the right.

User can interact with the form, create new entries, delete old ones and modify the existing ones.
<rtf>"""
import sys
# from PyQt5 import QtWidgets, QtCore, QtGui # Qt5
from PySide2 import QtWidgets, QtCore, QtGui
from cute_mongo_forms.column import LineEditColumn
from cute_mongo_forms.row import ColumnSpec, Row
from cute_mongo_forms.container import List, FormSet, EditFormSet
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
Create collection
<rtf>"""
collection=SimpleCollection(
  filename="simple_test.db",
  row_classes=[PersonRow,PersonRowExtended]
  )
  
"""<rtf>
Next we create a list container.  The List class is Row agnostic.  It only knows how to create a label, using a Row entry.  The only method we need to overwrite is the one used to create a label:
<rtf>"""
class PersonList(List):
  
  def makeLabel(self,entry):
    try:
      st=entry["firstname"]+" "+entry["surname"]
    except KeyError:
      st="?"
    return st


"""<rtf>
The Qt program.  The *EditFormSet* container allows user to interact with the database (save, delete and create new records).
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
    self.formset=EditFormSet(collection=collection)
    
    # Get form's widget and set it's parent to the current main widget
    self.formset.widget.setParent(self.w)
    
    # Add formset to layout
    self.lay.addWidget(self.formset.widget)
    
    # Inform formset about the item in question.  "self.lis.widget" is a QListWidget instance.
    self.lis.widget.currentItemChanged. connect(self.formset.chooseForm_slot)
    
    # inform the list when a new record has been added, saved or deleted
    self.formset.signals.modified. connect(self.lis.update_slot)
    
"""<rtf>
Start the main Qt program
<rtf>"""
if (__name__=="__main__"):
  app=QtWidgets.QApplication([])
  gui=MyGui()
  gui.show()
  app.exec_()


 
