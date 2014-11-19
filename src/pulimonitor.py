#!/usr/bin/python2.6
# -*- coding: utf8 -*-
from __future__ import absolute_import

"""
"""
__author__      = "Jerome Samson"
__copyright__   = "Copyright 2014, Mikros Image"

import sys
import os
import time

from PyQt4 import QtGui
from PyQt4.QtGui import QApplication, QMainWindow, QColor, QTextCursor, QIcon, QAction
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QObject, pyqtSignal
from PyQt4.QtCore import qDebug
from PyQt4.QtCore import QSettings
from PyQt4.QtCore import QPoint, QSize

#
#
#
from pulitools.common import XLogger, OutLog
from pulitools.pulimonitor.widgets.jobview import Job
from pulitools.pulimonitor.widgets.jobview import JobConfig
from pulitools.pulimonitor import Config



class PuliMonitor(QMainWindow):
    """
    """

    # LOGDIR = "/s/apps/lin/vfx_test_apps/pulistats/"
    # SRCDIR = "/datas/jsa/OpenRenderManagement/"
    # BASEDIR = "/s/apps/lin/puli/"

    def __init__(self):
        QMainWindow.__init__(self)
        
        xlogger.debug("Starting log")
        self.initIcon()
        self.initAction()
        self.initUI()
        xlogger.debug("UI loaded")

        data = {
            "items": [
                {
                    "id": 748291, 
                    "name": "[Katana|RenderShot] s0660_p0050_lit_v085 (L30/L41)", 
                    "status": 20, 
                    "completion": 0.1, 
                    "prod": "ddd", 
                    "shot": "s0660_p0050", 
                    "user": "mso", 

                    "items": [
                        {
                            "status": 2, 
                            "completion": 0.5, 
                            "prod": "ddd", 
                            "shot": "s0660_p0050", 
                            "name": "[Katana] Render s0660_p0050_lit_v085 L30 (s0660_p0050_L30|stereo)", 
                            "id": 748295, 
                            "user": "mso", 
                        }, 
                        {
                            "status": 0, 
                            "completion": 0.0, 
                            "prod": "ddd", 
                            "shot": "s0660_p0050", 
                            "name": "[report] Render s0660_p0050_lit_v085 L30 (s0660_p0050_L30|stereo) : render report", 
                            "id": 748296, 
                            "user": "mso", 
                        "items": [
                            {
                                "status": 2, 
                                "completion": 5, 
                                "prod": "ddd", 
                                "shot": "zdazdazd", 
                                "name": "[Katana]tereo)", 
                                "id": 748295, 
                                "user": "mso", 
                            }, 
                            {
                                "status": 0, 
                                "completion": 0.0, 
                                "prod": "ddd", 
                                "shot": "s0660_p0050", 
                                "name": "[report]render report", 
                                "id": 748296, 
                                "user": "mso", 
                            }
                        ], 
                        }

                    ], 
                },
                {
                    "id": 748290, 
                    "name": "[Katana|RenderShot]/L41)", 
                    "status": 1, 
                    "completion": 0.32, 
                    "prod": "ddd", 
                    "shot": "s0660_p0050", 
                    "user": "mso", 

                    "items": [
                        {
                            "status": 0, 
                            "completion": 0.0, 
                            "prod": "ddd", 
                            "shot": "s0660_p0050", 
                            "name": "[report] Render s0660_p0050_lit_v085 L30 (s0660_p0050_L30|stereo) : render report", 
                            "id": 748296, 
                            "user": "mso", 
                        }
                    ], 
                },
                {
                    "id": 748289, 
                    "name": "[Katana|RenderShot]/L41)", 
                    "status": 3, 
                    "completion": 0.45, 
                    "prod": "ddd", 
                    "shot": "s0660_p0050", 
                    "user": "mso", 
                }

            ], 
            "summary": {
                "count": 1, 
                "totalInDispatcher": 2323, 
                "requestTime": 0.0023128986358642578, 
                "requestDate": "Tue Oct 14 12:07:56 2014"
            }
        }

        self.jobs.loadData( data )
        xlogger.debug("Test Data loaded")
        
        self.readSettings()
        xlogger.debug("Settings restored")



    def initIcon(self):
        """
        """
        pass


    def initAction(self):
        """
        """

        self.testIconAction = QtGui.QAction( self.style().standardIcon( QtGui.QStyle.SP_FileDialogInfoView ), 'Show standard icons', self)
        self.testIconAction.triggered.connect( self.showStandardIcons )

        self.prefsEditAction = QtGui.QAction('Preferences', self)
        self.prefsEditAction.triggered.connect( self.prefsEdit )
        self.prefsEditAction.setShortcut('Ctrl+p')
        self.prefsEditAction.setStatusTip('Edit application preferences')

        self.aboutAction = QtGui.QAction('About', self)
        self.aboutAction.triggered.connect( self.about )


    def initUI(self):
        """
        """
        #
        # Menu
        #
        menubar = self.menuBar()
        
        editMenu = menubar.addMenu('&Edit')
        editMenu.addAction(self.prefsEditAction)

        helpMenu = menubar.addMenu('&Help')
        helpMenu.addAction(self.aboutAction)

        #
        # Toolbar
        #
        toolbar = self.addToolBar('')
        toolbar.addAction(self.testIconAction)

        #
        # Widgets
        #
        self.jobs = Job( self, JobConfig() )
        self.setCentralWidget(self.jobs)

        pass

    def closeEvent(self, pEvent):
        """
        """
        self.writeSettings()
        pEvent.accept()
        xlogger.info("Bye")

    def readSettings( self ):
        settings = QSettings(Config.qt_company_name, Config.qt_app_name)
        pos = settings.value("pos", QPoint(200, 200)).toPoint()
        size = settings.value("size", QSize(1280, 720)).toSize()
        self.resize(size)
        self.move(pos)

        prefs = QSettings(Config.qt_company_name, Config.qt_app_name).value("jobview_prefs")
        self.jobs.loadPrefs( prefs )

        # internal state also ?
        # self.restoreState()

    def writeSettings( self ):
        settings = QSettings(Config.qt_company_name, Config.qt_app_name)
        settings.setValue("pos", self.pos())
        settings.setValue("size", self.size())
        settings.setValue("jobview_prefs", self.jobs.prefs())

    def pause(self):
        import time
        time.sleep(.5)


    #################################################################################
    #
    # ACTIONS
    #
    def showStandardIcons(self):
        from pulitools.pulimonitor.widgets.standardicondialog import StandardIconDialog
        icons = StandardIconDialog(self)
        icons.show()        

    def prefsEdit(self):
        from pulitools.pulimonitor.widgets.prefsedit import PrefsEditDialog
        prefs = PrefsEditDialog(self, self.jobs.config)
        prefs.btnBox.button(QtGui.QDialogButtonBox.Apply).clicked.connect( self.jobs.onPrefChanged )
        prefs.btnBox.accepted.connect( self.jobs.onPrefChanged )
        prefs.show()
        pass

    def about(self):
        ''' About dialog
               <li>Qt: %s</li>
               <li>PyQt: %s</li>
               <li>sip: %s</li>

        '''

        from PyQt4.Qt import PYQT_VERSION_STR
        from PyQt4.QtCore import QT_VERSION_STR
        from sip import SIP_VERSION_STR

        msg = '''
            <h3>%s</h3>
            <span>v%s</span>

            <h4>Dependencies</h4>
            <table>
                <tr><td>Qt</td><td>%s</td></tr>
                <tr><td>PyQt</td><td>%s</td></tr>
                <tr><td>Sip</td><td>%s</td></tr>
            </table>
            ''' % (
                Config.qt_app_name, 
                Config.version, 
                QT_VERSION_STR, 
                PYQT_VERSION_STR, 
                SIP_VERSION_STR
            )


        QtGui.QMessageBox.about(self, 'About %s' % Config.qt_app_name, msg)
        pass


#################################################################################
# MAIN
if __name__ == '__main__':

    app = QApplication(sys.argv)

    # Used to create/maintain application settings
    app.setOrganizationName(Config.qt_company_name)
    app.setApplicationName(Config.qt_app_name)
    app.setWindowIcon( QIcon(Config.root_dir+"/rsrc/monitor.png"))

    #
    # Define logs
    # - user log streamed to a widget and stdout
    # - dev log streamed to a stdout
    xlogger = XLogger()

    monitor = PuliMonitor()
    monitor.show()

    app.exec_()