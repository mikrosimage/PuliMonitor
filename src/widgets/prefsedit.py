#!/usr/bin/python
# -*- coding: utf8 -*-
from __future__ import absolute_import

"""
"""
__author__      = "Jerome Samson"
__copyright__   = "Copyright 2014, Mikros Image"

import copy

from PyQt4 import QtGui
from PyQt4.QtCore import Qt
# from PyQt4.QtGui import QDialog
from pulitools.common import XLogger



class PrefsEditDialog(QtGui.QDialog):
    '''
    '''
    
    def __init__(self, parent, config):

        super(self.__class__, self).__init__(parent)
        
        self.config = config
        self.previousConfig = copy.copy(config)

        self.initUi()

    def initUi(self):

        ''' init user interface at startup
        '''
        self.layout = QtGui.QVBoxLayout()
        self.setLayout( self.layout )
        self.setWindowTitle('Preferences')

        self.list = QtGui.QListWidget( self )
        self.layout.addWidget( self.list )

        self.btnBox = QtGui.QDialogButtonBox( 
                                                QtGui.QDialogButtonBox.Ok | 
                                                QtGui.QDialogButtonBox.Cancel | 
                                                QtGui.QDialogButtonBox.Apply | 
                                                QtGui.QDialogButtonBox.RestoreDefaults 
                                            )

        self.layout.addWidget( self.btnBox )

        #
        # Connect
        #
        self.btnBox.button(QtGui.QDialogButtonBox.Apply).clicked.connect( self.updateConfig )
        self.btnBox.button(QtGui.QDialogButtonBox.RestoreDefaults).clicked.connect( self.restoreConfig )
        self.btnBox.accepted.connect( self.accept )
        self.btnBox.rejected.connect( self.cancel )

        # Populate list with config coming from main window's job treewidget
        for column in self.config.columns:
            item = QtGui.QListWidgetItem( column["label"], self.list, 0)
            item.setFlags( item.flags() | Qt.ItemIsUserCheckable)

            # print "field: %s" % (column)
            if column.get("hidden", False):
                item.setCheckState(Qt.Unchecked)
            else:
                item.setCheckState(Qt.Checked)

            self.list.addItem( item )
        self.list.item(0).setHidden(True)

    def refreshList(self):
        # XLogger().debug("Refresh list")

        for i,column in enumerate(self.config.columns):
            if column.get('hidden', False):
                self.list.item(i).setCheckState(Qt.Unchecked)
            else:
                self.list.item(i).setCheckState(Qt.Checked)
        pass

    def restoreConfig(self):
        '''
        '''

        XLogger().debug("Restore default columns")
        
        from pulitools.pulimonitor.widgets.jobview import JobConfig

        for i, header in enumerate(JobConfig.defaultColumns):
            hide = header.get('hidden',False)
            # XLogger().debug( " %1s %s" % ( '' if hide else '*', header['field'] ) )

            self.config.columns[i]['hidden']=header.get('hidden', False)
        
        self.refreshList()

    def updateConfig(self):
        '''
        '''
        XLogger().debug("Update jobs config")
        for i in xrange(self.list.count()):
            hide = True if (self.list.item(i).checkState() == Qt.Unchecked) else False
            # XLogger().debug( " %1s %s" % ( '' if hide else '*', self.list.item(i).text() ) )

            self.config.columns[i]['hidden']=hide


    def accept(self):
        XLogger().debug("Accept")
        self.updateConfig()
        self.refreshList()
        self.close()

    def cancel(self):
        XLogger().debug("Cancel")
        self.close()
        pass

    #def closeEvent(self, event):
    #    XLogger().debug("Close PrefsEditDialog")

