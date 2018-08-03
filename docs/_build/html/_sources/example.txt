
.. _example:

Example 
=======

Running the example
-------------------

You can try this example like this:

::

  ipython3
  from cute_mongo_forms.example import main
  main()
  
You can find the example's source code with:

:: 

  ipython3
  import cute_mongo_forms
  print(cute_mongo_forms.__file__)
  

The problem: parking area control
---------------------------------

So, you've done the tutorial and are ready for a more complex example.

We want a data model and a system of menus and forms for controlling the space of a corporate parking area.  The specifications of the system are:

- There are several parking areas.  
- Each parking area has a limited number of parking lots.  
- Certain vehicles can only access certain parking areas (during morning or evening).
- Each vehicle is associated to a company and to an individual

The system monitors the entering and leaving cars by cameras ("devices") that are installed both into the entrance and the exit of each parking area.  They register license plates of cars and register which car is parked at which parking area.


Document schema
---------------

The schema and relations for this problem look like this:

.. image:: images/license_plate.svg.png
   :width: 40 % 

   
Implementation
--------------

The schema definitions in the example's *DataModel* class looks like this:

::

  class DataModel:
    ...
    ...
    
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
      
