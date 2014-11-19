#!/usr/bin/python
# -*- coding: utf8 -*-
from __future__ import absolute_import

"""
"""
__author__      = "Jerome Samson"
__copyright__   = "Copyright 2014, Mikros Image"

import sys
import copy
from types import *

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QTableWidget, QTableWidgetItem, QTreeWidgetItem, QTreeWidget
from PyQt4.QtCore import Qt, QVariant

from pulitools.common import XLogger
from pulitools import pulimonitor


# class CustomTable(QtGui.QTableWidget):

#     def __init__(self, parent, config):
#         super(CustomTable, self).__init__( parent )
#         self.config = config


#     def setupFormat(self):
#         XLogger().debug("Setup table format with %s" % self.config)
        
#         # Init columns
#         self.setColumnCount(len(self.config.columns))

#         # Create header items
#         for i,header in enumerate(self.config.columns):
#             item = QTableWidgetItem(header["label"])
#             item.setTextAlignment(header.get("align",Qt.AlignCenter))
#             self.setHorizontalHeaderItem(i, item)
#             self.setColumnHidden(i, not header.get("visible",True))

#         # Expand last column
#         self.horizontalHeader().setStretchLastSection(True)


#     def addRow(self, row):
#         XLogger().debug( str(row ) )
#         rowNum = self.rowCount()
#         self.setRowCount( rowNum+1 )

#         # Create header items
#         # import pudb;pu.db
#         for i,header in enumerate(self.config.columns):
#             print row[header["field"]]
#             item = QTableWidgetItem(str(row[header["field"]]))
#             # item.setText(str(row[header["field"]]))
#             self.setItem(rowNum,i, item)

# class StandardDelegate(QtGui.QStyledItemDelegate):
#     def __init__(self, app, parent=None):
#         super(self.__class__, self ).__init__(parent)
 
#     def paint(self, painter, option, index):
#         option.font.setWeight(QtGui.QFont.Normal)
#         super(self.__class__, self).paint(painter, option, index)
  

# class BoldDelegate(QtGui.QStyledItemDelegate):
#     def __init__(self, app, parent=None):
#         super(self.__class__, self ).__init__(parent)

#     def paint(self, painter, option, index):
#         option.font.setWeight(QtGui.QFont.Bold)
#         super(self.__class__, self).paint(painter, option, index)

class CustomDisplay(object):

    @staticmethod
    def default(item, fieldColumn, fieldValue, *args):
        # XLogger().debug("default( column=%s, value=%s, args=%r )" % (fieldColumn, fieldValue, args) )
        item.setText( fieldColumn, str(fieldValue) )

    @staticmethod
    def status(item, fieldColumn, fieldValue, *args):
        # XLogger().debug("status( column=%s, value=%s, args=%r )" % (fieldColumn, fieldValue, args) )
        from octopus.core.enums.node import NODE_STATUS_NAMES

        try:
            name = NODE_STATUS_NAMES[fieldValue]    
        except IndexError,e:
            name = "UNDEFINED"

        if name == "BLOCKED":
            color = QtGui.QColor("lightGray")
        elif name == "READY":
            color = QtGui.QColor("lightYellow")
        elif name == "RUNNING":
            color = QtGui.QColor("lightBlue")
        elif name == "DONE":
            color = QtGui.QColor("lightGreen")
        elif name == "ERROR":
            color = QtGui.QColor("lightRed")
        elif name == "CANCELED":
            color = QtGui.QColor("darkGray")
        elif name == "PAUSED":
            color = QtGui.QColor("darkYellow")
        else:
            color = None

        item.setText( fieldColumn, str(name) )

        # Change font
        font = item.font( fieldColumn )
        font.setWeight( QtGui.QFont.Bold )
        item.setFont( fieldColumn, font )

        if color:
            brush = QtGui.QBrush( color )
            item.setBackground( fieldColumn, brush )

    # @staticmethod
    # def dateToStr(pValue):
    #     if datetime.now().day == datetime.fromtimestamp( pValue ).day:
    #         result = datetime.strftime( datetime.fromtimestamp( float(pValue) ), Settings.time_format )
    #     else:
    #         result = datetime.strftime( datetime.fromtimestamp( float(pValue) ), Settings.date_format )
    #     return str(result)

    # @staticmethod
    # def preciseDateToStr(pValue):
    #     if datetime.now().day == datetime.fromtimestamp( pValue ).day:
    #         result = datetime.strftime( datetime.fromtimestamp( float(pValue) ), Settings.precise_time_format )
    #     else:
    #         result = datetime.strftime( datetime.fromtimestamp( float(pValue) ), Settings.precise_date_format )
    #     return str(result)

    # @staticmethod
    # def listToStr(pValue):
    #     return ", ".join(pValue)



class JobConfig(object):
    defaultColumns = [
            { "field":"childIndicator",     "label":"",                 },
            { "field":"id",                 "label":"Id",               },
            { "field":"status",             "label":"Status",           "formula":["CustomDisplay.status"]},
            { "field":"name",               "label":"Name",             },
            { "field":"completion",         "label":"Progress",         "formula":["progressBar"] },
            { "field":"prod",               "label":"Prod",             },
            { "field":"shot",               "label":"Shot",             },
            { "field":"user",               "label":"Owner",            "hidden":False },
            { "field":"dispatchKey",        "label":"Prio",             "hidden":True },
            { "field":"commandCount",       "label":"Total",            "hidden":True },
            { "field":"readyCommandCount",  "label":"Ready",            "hidden":True },
            { "field":"doneCommandCount",   "label":"Done",             "hidden":True },
            { "field":"optimalMaxRN",       "label":"MAXRN-optimal",    "hidden":True },
            { "field":"maxRN",              "label":"MAXRN-real",       "hidden":True },
            { "field":"allocatedRN",        "label":"Allocated RN",     "hidden":True },
            { "field":"maxAttempt",         "label":"Attempts",         "hidden":True },
            { "field":"creationTime",       "label":"Submitted",        "hidden":True },
            { "field":"startTime",          "label":"Start",            "hidden":True },
            { "field":"endTime",            "label":"End",              "hidden":True },
            { "field":"runTime",            "label":"Run time",         "hidden":True },
            { "field":"averageTimeByFrame", "label":"Avg time",         "hidden":True },
        ]


    def __init__(self):
        self.columns = copy.deepcopy(JobConfig.defaultColumns)
        pass




class CustomTree(QtGui.QTreeWidget):

    def __init__(self, parent, config):
        super(CustomTree, self).__init__( parent )
        self.config = config


    #
    # Specific display methods
    #
    def default(self, item, fieldColumn, fieldValue, *args):
        # XLogger().debug("default( column=%s, value=%s, args=%r )" % (fieldColumn, fieldValue, args) )
        item.setText( fieldColumn, str(fieldValue) )

    def progressBar(self, item, fieldColumn, fieldValue, *args):
        # XLogger().debug("progressBar( column=%s, value=%s, args=%r )" % (fieldColumn, fieldValue, args) )

        tmp = QtGui.QProgressBar(self)
        tmp.setValue( float(fieldValue)*100 )
        self.setItemWidget(item, fieldColumn, tmp)


    #
    # Slots
    #
    @QtCore.pyqtSlot()
    def onPrefChanged(self):
        '''
        Slot called when the internal config has been changed. Calls the refreshVisibility method to apply changes for each column
        '''
        XLogger().debug("onPrefChanged received")
        self.refreshVisibility()


    def refreshVisibility(self):
        for i,header in enumerate(self.config.columns):
            hiddenFlag = header.get("hidden", False)
            self.setColumnHidden(i, hiddenFlag)
            # self.resizeColumnToContents(i)
        pass

    def setHeaders(self):
        if not self.config:
            return False

        headerNames = []
        for i,header in enumerate(self.config.columns):
            headerNames.append( header["label"] )

        self.setHeaderLabels( headerNames )

    def setupFormat(self):
        XLogger().debug("Init table format with standard class: %s" % self.config)

        # Init columns
        self.setColumnCount(len(self.config.columns))
        self.setHeaders()
        self.refreshVisibility()
        

    def setItemValues(self, item, row):
        """
        Set a text, widget or other delegate to each columns of the given item
        The display particularity is defined in each column in the "formula" key.
        A "formula" is a list containing at list 1 element: the name of the method to use.
        Any other element in the list will be send as args to the method.
        The formula can call a method of the current instance or a method of any object defined in the scope
        """

        # Loop over each column of this row
        for i,data in enumerate(self.config.columns[1:]):

            if not('formula' in data):
                # This column has no formula, use "CustomTree.default" method with no args
                method = self.default
                args = []
            else:
                # With a formula attribute, we check if the first item of the list targets a method of the current instance 
                # or the method of another object

                if '.' in data['formula'][0]:
                    # We must identify a class and its method
                    clsName, methodName = data['formula'][0].split('.',1)
                    method = getattr( getattr(sys.modules[__name__],clsName), methodName )
                else:
                    # We call a method of our CustomTree class
                    methodName = data['formula'][0]
                    method = getattr( self, methodName )

                # Create args with remaining elements of the formula list
                args = data['formula'][1:]


            #
            # Actual call for the current item and column
            #
            if not callable(method):
                XLogger().error("Error formula must be a static method of CustomDisplay class")
            else:
                value = row.get(data['field'],'')
                method(item, i+1, value, *args)



    def addItem(self, parent, data):
        """
        Add row as an item attached to a parent item
        """
        item = QTreeWidgetItem(parent)
        # item.setIcon( 0, QtGui.QIcon( pulimonitor.Config.root_dir+"/rsrc/network.png" ) )
        self.setItemValues( item, data )

        if "items" in data:
            for child in data["items"]:
                self.addItem( item, child)

        parent.addChild( item )


    def addRow(self, row):
        """
        Add row as a new root item
        """
        root = QTreeWidgetItem(self)
        root.setIcon( 0, QtGui.QIcon( pulimonitor.Config.root_dir+"/rsrc/graph_32.png" ) )

        # self.bold = BoldDelegate(self)
        # self.standard = StandardDelegate(self)
        # self.setItemDelegateForColumn(4, self.bold)
        # self.setItemDelegateForColumn(5, self.standard)

        self.setItemValues( root, row )
        if "items" in row:
            for item in row["items"]:
                self.addItem( root, item)


    def loadPrefs(self, prefs):
        ''' Restore the header view state with app settings
        - use the widget 'restoreState's method with given headerViewState
        - update config.column with given visibility array [{'name','hiddenFlag'}]
        - refresh instance's visibility

        @param prefs: QVariant( (headerViewState, visibility) )
        '''

        prefs = prefs.toPyObject()

        if not prefs:
            XLogger().info("No prefs to load for %s" % self.__class__.__name__)
            return
        
        self.header().restoreState( prefs[0] )
    
        for name, hidden in prefs[1]:
            for col in self.config.columns:
                if col["field"]==name:
                    col["hidden"] = hidden

        self.refreshVisibility()
        pass

    def prefs(self):
        ''' Returns a QByteArray representing the header view state '''
        heaverViewState = self.header().saveState()
        visibilityFlags = [(elem.get("field",''),elem.get("hidden",True)) for i,elem in enumerate(self.config.columns)]
        return (heaverViewState, visibilityFlags)
        pass

class Job(CustomTree):
    '''
    '''
    
    def __init__(self, parent, config):
        super(Job, self).__init__(parent, config)
        self.initUi()

    def initUi(self):
        ''' init user interface at startup
        '''
        super(self.__class__, self).setupFormat()

        self.setSortingEnabled(True)
                

    def loadData(self, data):

        if "items" in data:
            for row in data["items"]:
                self.addRow(row)
        pass

