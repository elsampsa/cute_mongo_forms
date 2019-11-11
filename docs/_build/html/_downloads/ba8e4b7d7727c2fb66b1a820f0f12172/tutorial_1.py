"""<rtf>
In this lesson, we define a Row.  We use the Row's autogenerated form and use it in the main Qt program.  In this example, there is not yet any interaction with the database.

Let's start by importing all necesary modules.
<rtf>"""
import sys
# from PyQt5 import QtWidgets, QtCore, QtGui # Qt5
from PySide2 import QtWidgets, QtCore, QtGui # Qt5
from cute_mongo_forms.column import LineEditColumn
from cute_mongo_forms.row import ColumnSpec, Row
from cute_mongo_forms.db import SimpleCollection

"""<rtf>
Next we create a custom row (a column pattern).  All custom rows are subclasses of the base class Row.

The column pattern of a row is a list of ColumnSpec instances, where the first argument is the column type (in this case "LineEditColumn").  *key_name* is the key value stored in the document (in the key/value pair) and *label_name* is the name used in the Qt form.

Like this:
<rtf>"""
class PersonRow(Row):
  
  columns=[
    ColumnSpec(LineEditColumn, key_name="firstname", label_name="First Name"),
    ColumnSpec(LineEditColumn, key_name="surname",   label_name="Surname"),
    ColumnSpec(LineEditColumn, key_name="address",   label_name="Address")
  ]
"""<rtf>
Each row structure (e.g., **PersonRow**), has a corresponding graphical user interface form that is autogenerated.
<rtf>"""

"""<rtf>
In the main Qt program, we instantiate the PersonRow and use it's form widget
<rtf>"""
class MyGui(QtWidgets.QMainWindow):


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
    self.lay=QtWidgets.QHBoxLayout(self.w)
    
    # Instantiate the row
    self.row=PersonRow()
    
    # Get row's form widget
    self.row.widget.setParent(self.w)
    
    # .. and add it to the main layout
    self.lay.addWidget(self.row.widget)
    
"""<rtf>
Start the main Qt program
<rtf>"""
if (__name__=="__main__"):
  app=QtWidgets.QApplication([])
  gui=MyGui()
  gui.show()
  app.exec_()

