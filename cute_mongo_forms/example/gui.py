import sys
# from PyQt5 import QtWidgets, QtCore, QtGui # Qt5
from PySide2 import QtWidgets, QtCore, QtGui
from cute_mongo_forms.column import LineEditColumn, ListEditColumn, CheckBoxColumn
from cute_mongo_forms.row import ColumnSpec, Row
from cute_mongo_forms.container import List, FormSet, EditFormSet
from cute_mongo_forms.db import SimpleCollection
from cute_mongo_forms.example.datamodel import DataModel, ListAndForm, PermissionListsAndForm
# from bson import ObjectId


class MyGui(QtWidgets.QMainWindow):


  def __init__(self,parent=None):
    super(MyGui, self).__init__()
    self.initVars()
    self.setupUi()
    
    
  def initVars(self):
    # Connect to db, define column patters (i.e. rows), 
    self.data_model=DataModel()
    self.data_model.purge()
    
    
  def setupUi(self):
    self.setGeometry(QtCore.QRect(100,100,800,800))
    self.w=QtWidgets.QWidget(self)
    self.setCentralWidget(self.w)
    self.lay=QtWidgets.QHBoxLayout(self.w)
    
    self.person_view  =ListAndForm(self.data_model.getPersonList(), self.data_model.getPersonForm(),  "Registered Persons",  self.w)
    self.vehicle_view =ListAndForm(self.data_model.getVehicleList(),self.data_model.getVehicleForm(), "Registered Vehicles", self.w)
    self.device_view  =ListAndForm(self.data_model.getDeviceList(), self.data_model.getDeviceForm(),  "Registered Cameras",  self.w)
    self.company_view =ListAndForm(self.data_model.getCompanyList(),self.data_model.getCompanyForm(), "Registered Companies",self.w)
    self.area_view    =ListAndForm(self.data_model.getAreaList(),   self.data_model.getAreaForm(),    "Registered Areas",    self.w)
    
    self.area_permission_view  =PermissionListsAndForm("Area Permissions",          
                                                        self.data_model.getAreaList(),
                                                        self.data_model.getVehicleList(),
                                                        self.data_model.getAreaPermissionForm(),
                                                        titles=["AREA","VEHICLE","PERMISSION"],
                                                        parent=self.w)
    
    self.area_permission_per_company_view =PermissionListsAndForm("Area Permission per Company",
                                                                  self.data_model.getAreaList(),
                                                                  self.data_model.getCompanyList(),
                                                                  self.data_model.getAreaPerCompanyPermissionForm(),
                                                                  titles=["AREA","COMPANY","PERMISSION"],
                                                                  parent=self.w)
    
    # Update GUI's if relation targets change:
    self.device_view.modified. connect(self.area_view.update)
    self.vehicle_view.modified.connect(self.area_view.update)
    self.area_view.modified.   connect(self.area_permission_view.update)
    self.vehicle_view.modified.connect(self.area_permission_view.update)
    self.area_view.modified.   connect(self.area_permission_per_company_view.update)
    self.company_view.modified.connect(self.area_permission_per_company_view.update)
    
    self.all_views=[self.person_view, self.vehicle_view, self.device_view, self.company_view, self.area_view, self.area_permission_view, self.area_permission_per_company_view]
    
    self.hideAll()
    for view in self.all_views:
      self.lay.addWidget(view.widget)
    
    self.file_menu    =self.menuBar().addMenu("File")
    self.config_menu  =self.menuBar().addMenu("Configuration")
    self.perm_menu    =self.menuBar().addMenu("Permissions")
    
    self.exit_action           =self.file_menu.addAction("Exit")
    self.exit_action.triggered.connect(self.exit_slot)
    
    self.person_menu_action   =self.config_menu.addAction("Persons")
    self.vehicle_menu_action  =self.config_menu.addAction("Vehicles")
    self.device_menu_action   =self.config_menu.addAction("Devices")
    self.company_menu_action  =self.config_menu.addAction("Companies")
    self.area_menu_action     =self.config_menu.addAction("Areas")
    
    self.area_permissions_action =self.perm_menu.addAction("Area Permissions")
    self.area_per_company_action =self.perm_menu.addAction("Area per Company Permissions")
    
    self.person_menu_action.triggered.  connect(self.person_menu_slot)
    self.vehicle_menu_action.triggered. connect(self.vehicle_menu_slot)
    self.device_menu_action.triggered.  connect(self.device_menu_slot)
    self.company_menu_action.triggered. connect(self.company_menu_slot)
    self.area_menu_action.triggered.    connect(self.area_menu_slot)
    
    self.area_permissions_action.triggered. connect(self.area_permission_slot)
    self.area_per_company_action.triggered. connect(self.area_per_company_slot)
    
    
  def hideAll(self):
    for view in self.all_views:
      view.widget.hide()
  
  def person_menu_slot(self):
    print("persons menu!")
    self.hideAll()
    self.person_view.widget.show()
  
  def vehicle_menu_slot(self):
    print("vehicles menu!")
    self.hideAll()
    self.vehicle_view.widget.show()
    
  def device_menu_slot(self):
    print("devices menu!")
    self.hideAll()
    self.device_view.widget.show()
    
  def company_menu_slot(self):
    print("companies menu!")
    self.hideAll()
    self.company_view.widget.show()
    
  def area_menu_slot(self):
    print("areas menu!")
    self.hideAll()
    self.area_view.widget.show()
    
  def area_permission_slot(self):
    print("areas menu!")
    self.hideAll()
    self.area_permission_view.widget.show()
    
  def area_per_company_slot(self):
    print("companies per areas menu!")
    self.hideAll()
    self.area_permission_per_company_view.widget.show()
    
  def exit_slot(self):
    self.close()

  def closeEvent(self,e):
    self.data_model.close()
    e.accept()


def main():
  app=QtWidgets.QApplication([])
  gui=MyGui()
  gui.show()
  app.exec_()


if (__name__=="__main__"):
  main()
