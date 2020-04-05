"""
constant.py : Constant columns.  For example, a ComboBoxColumn with predefined values.

* Copyright: 2019 Sampsa Riikonen
* Authors  : Sampsa Riikonen
* Date     : 2019
* Version  : 0.7.1

This file is part of the cute_mongo_forms library

License: LGPLv3+ (see the COPYING.LESSER file)
"""

import sys
from PySide2 import QtWidgets, QtCore, QtGui
from cute_mongo_forms.column.base import Column
from cute_mongo_forms.tools import typeCheck, dictionaryCheck, objectCheck, parameterInitCheck, noCheck
pre_mod = __name__ # a string for aux debuggin purposes


class ConstantComboBoxColumn(Column):
    """A Column that can have a finite number of different values.  The possible values are defined by callback.

    Parameters at instantiation:

    :param key_name:              Key in the principal collection whose values correspond to keys in the foreign collection (in that example above key_name = key2)
    :param label_name:            Name of the drop-down list in the form widget
    """

    # define here, where the foreign key is mapped..
    parameter_defs = {
        "list"      : None, # list of tuples
        "callback"  : None  # should return a list of tuples (label, value)
    }
    parameter_defs.update(Column.parameter_defs)


    def __init__(self, **kwargs):
        # auxiliary string for debugging output
        self.pre = self.__class__.__name__ + " : "
        # check kwargs agains parameter_defs, attach ok'd parameters to this
        # object as attributes
        self.parameter_defs.update(super().parameter_defs)
        parameterInitCheck(self.parameter_defs, kwargs, self)
        self.makeWidget()
        self.reset()


    def getList(self):
        if self.callback is None:
            lis = self.list
        else:
            lis = self.callback()            
        assert(isinstance(lis,list))
        return lis


    def makeWidget(self):
        self.widget = QtWidgets.QComboBox()
        self.widget.clear()
        lis = self.getList()
        for i, (label, value) in enumerate(lis):
            self.widget.insertItem(i,
                label,
                value
            )

        # self.updateWidget()

    def updateWidget(self):
        """
        self.widget.clear()
        if self.callback is None:
            lis = self.list
        else:
            lis = self.callback()
        assert(isinstance(lis,list))
        for i, (label, value) in enumerate(lis):
            self.widget.insertItem(i,
                label,
                value
            )
        """
        self.widget.clear()
        lis = self.getList()
        for i, (label, value) in enumerate(lis):
            self.widget.insertItem(i,
                label,
                value
            )



    def getValue(self):
        # Get the value from QtWidget
        # self.widget.currenText()
        # self.widget.currentData()
        return self.widget.currentData()  # returns the foreign key

    def setValue(self, value):
        # if value is not found 
        # findData returns -1 setCurrentIndex(-1) sets the selection to void
        i = self.widget.findData(value)
        self.widget.setCurrentIndex(i)

    def reset(self):
        self.widget.setCurrentIndex(-1)


class ConstantRadioButtonColumn(Column):
    """A Column that can have a finite number of different values.  The possible values are defined by callback.

    Parameters at instantiation:

    :param key_name:              Key in the principal collection whose values correspond to keys in the foreign collection (in that example above key_name = key2)
    :param label_name:            Name of the drop-down list in the form widget
    """

    # define here, where the foreign key is mapped..
    parameter_defs = {
        "list"      : None, # list of tuples
        "callback"  : None, # should return a list of tuples (label, value)
        "label_alignment"   : None, # QtCore.Qt.AlignTop
        "label_size_policy" : None # QtWidgets.QSizePolicy()
    }

    def __init__(self, **kwargs):
        # auxiliary string for debugging output
        self.pre = self.__class__.__name__ + " : "
        # check kwargs agains parameter_defs, attach ok'd parameters to this
        # object as attributes
        self.parameter_defs.update(super().parameter_defs)
        parameterInitCheck(self.parameter_defs, kwargs, self)

        self.label_alignment = QtCore.Qt.AlignTop

        self.makeWidget()
        self.reset()


    def getList(self):
        if self.callback is None:
            lis = self.list
        else:
            lis = self.callback()            
        assert(isinstance(lis,list))
        return lis


    def makeWidget(self):
        self.widget = QtWidgets.QWidget()
        # self.widget.setAlignment(QtCore.Qt.AlignTop) # nopes
        self.sublay = QtWidgets.QVBoxLayout(self.widget)
        self.sublay.setAlignment(QtCore.Qt.AlignTop)

        lis = self.getList()
        self.radio_buttons_by_value = {}
        # policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        policy = QtWidgets.QSizePolicy()
        policy.setVerticalPolicy(QtWidgets.QSizePolicy.Minimum)
        # policy.setVerticalPolicy(QtWidgets.QSizePolicy.ShrinkFlag)
        self.widget.setSizePolicy(policy)
        # self.widget.setMaximumHeight(40)

        for i, (label, value) in enumerate(lis):
            # print("ConstantRadioButtonColumn: makeWidget: label, value>", label, value)
            rb = QtWidgets.QRadioButton(label, self.widget)
            # rb = QtWidgets.QLabel("test")
            rb.setSizePolicy(policy)
            self.radio_buttons_by_value[value] = rb
            self.sublay.addWidget(rb)
        self.updateWidget()


    def __getitem__(self, key):
        return self.radio_buttons_by_value[key]


    def updateWidget(self):
        pass


    def getValue(self):
        # Get the value from QtWidget
        # self.widget.currenText()
        # self.widget.currentData()
        #print(self.pre, "getValue")
        for value, rb in self.radio_buttons_by_value.items():
            #print(self.pre, "getValue", value)
            # if rb.isDown():
            if rb.isChecked():
                return value
        return None # none selected

    def setValue(self, value):
        # if value is not found 
        # findData returns -1 setCurrentIndex(-1) sets the selection to void
        try:
            rb = self.radio_buttons_by_value[value]
        except KeyError:
            # raise
            return
        #print(self.pre, "setValue:", value, rb)
        # rb.setDown(True)
        rb.setChecked(True)


    def reset(self):
        value = self.getList()[0][1] # value
        self.setValue(value)





    
def test1():
  st="""Empty test
  """
  pre=pre_mod+"test1 :"
  print(pre,st)
  

def test2():
  st="""Empty test
  """
  pre=pre_mod+"test2 :"
  print(pre,st)
  

def main():
  pre=pre_mod+"main :"
  print(pre,"main: arguments: ",sys.argv)
  if (len(sys.argv)<2):
    print(pre,"main: needs test number")
  else:
    st="test"+str(sys.argv[1])+"()"
    exec(st)
  
  
if (__name__=="__main__"):
  main()

