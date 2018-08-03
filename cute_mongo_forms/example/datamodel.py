import sys
# from PyQt5 import QtWidgets, QtCore, QtGui # Qt5
from PySide2 import QtWidgets, QtCore, QtGui
from cute_mongo_forms.column import LineEditColumn, ListEditColumn, CheckBoxColumn, ForeignKeyColumn
from cute_mongo_forms.row import ColumnSpec, Row
from cute_mongo_forms.container import List, FormSet, EditFormSet, PermissionFormSet
from cute_mongo_forms.db import MongoCollection


class ListAndForm:
  """Creates a composite widget using a List and a FormSet
  """
  
  def __init__(self,lis,form,title="",parent=None):
    self.title=title
    self.lis  =lis
    self.form =form
    
    self.widget =QtWidgets.QWidget(parent) # create a new widget
    self.lay  =QtWidgets.QVBoxLayout(self.widget) # attach layout to that widget
    self.label=QtWidgets.QLabel(self.title,self.widget)
    
    self.subwidget=QtWidgets.QWidget(self.widget)
    self.sublay   =QtWidgets.QHBoxLayout(self.subwidget)
    
    self.lay.addWidget(self.label)
    self.lay.addWidget(self.subwidget)
    
    self.lis. widget.setParent(self.subwidget) # get widget from List and set its parent to widget
    self.form.widget.setParent(self.subwidget)
    self.sublay. addWidget(self.lis.widget) # add List's internal widget to widget's layout
    self.sublay. addWidget(self.form.widget)
    self.lis.widget.currentItemChanged. connect(self.form.chooseForm_slot) # connections between list and the form
    self.form.signals.modified.connect(self.lis.update_slot)
    self.modified =self.form.signals.modified # shorthand


  def update(self):
    """Widgets might have drop-down menus and sublists that depend on other document collections
    """
    self.form.updateWidget()


class PermissionListsAndForm:
  """Encapsulates two lists and a PermissionFormSet linking them
  """
  
  def __init__(self,maintitle,lis1,lis2,form,titles=["","",""],parent=None):
    self.maintitle=maintitle
    self.lis1 =lis1
    self.lis2 =lis2
    self.form =form
    self.titles=titles
    self.parent=parent
    
    self.widget =QtWidgets.QWidget(parent) # create a new widget
    self.lay    =QtWidgets.QHBoxLayout(self.widget) # attach layout to that widget
    
    # create three subwidgets
    self.sections=[]
    self.layouts =[]
    self.labels  =[]
    for i in range(0,3):
      self.sections.append(QtWidgets.QWidget(self.widget)) # create a widget
      self.layouts .append(QtWidgets.QVBoxLayout(self.sections[-1])) # .. create a layout to that widget
      self.labels  .append(QtWidgets.QLabel(titles[i],self.sections[-1])) # add a QLabel to the widget
      self.layouts[-1].addWidget(self.labels[-1]) # add the QLabel to widget's layout
      self.lay.addWidget(self.sections[-1]) # add the widget to main layout
  
    self.lis1.widget.setParent(self.sections[0])
    self.layouts[0].addWidget(self.lis1.widget)

    self.lis2.widget.setParent(self.sections[1])
    self.layouts[1].addWidget(self.lis2.widget)
    
    self.form.widget.setParent(self.sections[2])
    self.layouts[2].addWidget(self.form.widget)
    
    # Connect the user/car pair to the permission form
    self.lis1.widget. currentItemChanged. connect(self.form.chooseRecord1_slot) # inform form about the item in question
    self.lis2.widget. currentItemChanged. connect(self.form.chooseRecord2_slot) # inform form about the item in question
    
  
  def update(self):
    """Tell the lists to update their contents
    """
    self.lis1.update_slot(None) # re-read list and set current item to None
    self.lis2.update_slot(None)


class DataModel:
    
  def __init__(self):
    self.define()
    self.defineGUI()
  
  
  def close(self):
    # print("close: ",self.area_rights_collection)
    for collection in self.collections:
      collection.close()
  
  
  def clear(self,yes_really_do_it=False):
    if (yes_really_do_it==False):
      print("DataModel: WARNING! about to annihilate the database.  But you were not confident enough..")
      return
    for collection in self.collections:
      collection.clear()
  
  
  def purge(self):
    """For migrations / cleanup.  Collections should be in correct order.
    """
    for collection in self.collections:
      # print("purging",collection)
      collection.purge()
  
  
  def define(self):
    """Define column patterns and collections
    """
    self.db_name="cute_mongo_forms_example"
    self.collections=[]
  
    class PersonRow(Row):
      columns=[
        ColumnSpec(LineEditColumn, key_name="name",   label_name="Name"),
        ColumnSpec(LineEditColumn, key_name="surname",label_name="Surname"),
        ColumnSpec(LineEditColumn, key_name="phone",  label_name="Phone Number"),
        ColumnSpec(LineEditColumn, key_name="email",  label_name="E-mail")
      ]
    self.PersonRow=PersonRow
    self.person_collection =MongoCollection(database_name=self.db_name, collection_name="person", row_classes=[self.PersonRow])
    self.collections.append(self.person_collection)
    
    class CompanyRow(Row):
      columns=[
        ColumnSpec(LineEditColumn, key_name="name", label_name="Name")
        # could add here whatever company data.. address, phone number, etc.
      ]
    self.CompanyRow=CompanyRow
    self.company_collection =MongoCollection(database_name=self.db_name,collection_name="company",row_classes=[self.CompanyRow])
    self.collections.append(self.company_collection)
    
    class VehicleRow(Row):
      columns=[
        ColumnSpec(LineEditColumn,   key_name="license_plate", label_name="License Plate"),
        ColumnSpec(LineEditColumn,   key_name="brand",         label_name="Brand"),
        ColumnSpec(LineEditColumn,   key_name="color",         label_name="Color"),
        ColumnSpec(ForeignKeyColumn, key_name="person_id",  collection=self.person_collection),
        ColumnSpec(ForeignKeyColumn, key_name="company_id", collection=self.company_collection)
      ]
    self.VehicleRow=VehicleRow
    self.vehicle_collection =MongoCollection(database_name=self.db_name,collection_name="vehicle",row_classes=[self.VehicleRow])
    self.collections.append(self.vehicle_collection)
    
    class DeviceRow(Row):
      columns=[
        ColumnSpec(LineEditColumn, key_name="url",        label_name="URL"),
        ColumnSpec(LineEditColumn, key_name="user",       label_name="User"),
        ColumnSpec(LineEditColumn, key_name="password",   label_name="Password"),
        ColumnSpec(LineEditColumn, key_name="description",label_name="Description")
      ]
    self.DeviceRow=DeviceRow
    self.device_collection =MongoCollection(database_name=self.db_name,collection_name="device",row_classes=[DeviceRow])
    self.collections.append(self.device_collection)
    
    class AreaRow(Row):
      columns=[
        ColumnSpec(LineEditColumn, key_name="name",       label_name="Name"),
        ColumnSpec(LineEditColumn, key_name="description",label_name="Description"),
        ColumnSpec(ListEditColumn, key_name="incoming", label_name="Cameras IN",  collection=self.device_collection,  foreign_label_name="url"),
        ColumnSpec(ListEditColumn, key_name="outgoing", label_name="Cameras OUT", collection=self.device_collection,  foreign_label_name="url"),
        ColumnSpec(LineEditColumn, key_name="max",      label_name="Max. vehicles"),
        ColumnSpec(ListEditColumn, key_name="parked",   label_name="Currently parked", collection=self.vehicle_collection, foreign_label_name="license_plate")
      ]
    self.AreaRow=AreaRow
    self.area_collection =MongoCollection(database_name=self.db_name,collection_name="area",row_classes=[self.AreaRow])
    self.collections.append(self.area_collection)
    
    class AreaRightsRow(Row):
      columns=[
        ColumnSpec(ForeignKeyColumn, key_name="vehicle_id", collection=self.vehicle_collection),
        ColumnSpec(ForeignKeyColumn, key_name="area_id",    collection=self.area_collection),
        ColumnSpec(CheckBoxColumn,   key_name="morning",  label_name="Can park in the morning"),
        ColumnSpec(CheckBoxColumn,   key_name="evening",  label_name="Can park in the evening")
      ]
    self.AreaRightsRow=AreaRightsRow
    self.area_rights_collection =MongoCollection(database_name=self.db_name,collection_name="area_rights",row_classes=[self.AreaRightsRow])
    self.collections.append(self.area_rights_collection)
    
    class AreaRightsPerCompanyRow(Row):
      columns=[
        ColumnSpec(ForeignKeyColumn, key_name="company_id", collection=self.company_collection),
        ColumnSpec(ForeignKeyColumn, key_name="area_id",    collection=self.area_collection),
        ColumnSpec(LineEditColumn, key_name="max",   label_name="Max. vehicles")
      ]
    self.AreaRightsPerCompanyRow=AreaRightsPerCompanyRow
    self.area_rights_per_company_collection =MongoCollection(database_name=self.db_name,collection_name="area_rights_per_company",row_classes=[self.AreaRightsPerCompanyRow])
    self.collections.append(self.area_rights_per_company_collection)
    

  def defineGUI(self):
    """Define forms, lists, etc.
    """
    
    # *** Simple lists ***
    class PersonList(List):
      def makeLabel(self,entry):
        try:
          st=entry["name"]+" "+entry["surname"]
        except KeyError:
          st="?"
        return st
    self.PersonList=PersonList
      
    class VehicleList(List):
      def makeLabel(self,entry):
        try:
          st=entry["license_plate"]+" ("+entry["color"]+" "+entry["brand"]+")"
        except KeyError:
          st="?"
        return st
    self.VehicleList=VehicleList
      
    class AreaList(List):
      def makeLabel(self,entry):
        try:
          st=entry["name"]+" ("+entry["description"]+")"
        except KeyError:
          st="?"
        return st
    self.AreaList=AreaList
    
    class CompanyList(List):
      def makeLabel(self,entry):
        try:
          st=entry["name"]
        except KeyError:
          st="?"
        return st
    self.CompanyList=CompanyList
    
    class DeviceList(List):
      def makeLabel(self,entry):
        try:
          st=entry["url"]+" ("+entry["description"]+")"
        except KeyError:
          st="?"
        return st
    self.DeviceList=DeviceList
    
  # methods for instantiating lists
  def getPersonList(self):
    return self.PersonList (collection=self.person_collection)
  
  def getVehicleList(self):
    return self.VehicleList(collection=self.vehicle_collection)
  
  def getCompanyList(self):
    return self.CompanyList(collection=self.company_collection)
  
  def getAreaList(self):
    return self.AreaList   (collection=self.area_collection)
  
  def getDeviceList(self):
    return self.DeviceList (collection=self.device_collection)
    
    
  # methods for instantiating forms
  def getPersonForm(self):
    return EditFormSet(collection=self.person_collection)
  
  def getVehicleForm(self):
    return EditFormSet(collection=self.vehicle_collection)
  
  def getCompanyForm(self):
    return EditFormSet(collection=self.company_collection)
  
  def getDeviceForm(self):
    return EditFormSet(collection=self.device_collection)
  
  def getAreaForm(self):
    return EditFormSet(collection=self.area_collection)
    
  def getAreaPermissionForm(self):
    return PermissionFormSet(collection=self.area_rights_collection, key1_name="area_id", key2_name="vehicle_id")
  
  def getAreaPerCompanyPermissionForm(self):
    return PermissionFormSet(collection=self.area_rights_per_company_collection, key1_name="company_id", key2_name="area_id")
    


