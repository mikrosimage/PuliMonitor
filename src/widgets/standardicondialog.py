#!/usr/bin/python
# -*- coding: utf8 -*-
from __future__ import absolute_import

"""
"""
__author__      = "Jerome Samson"
__copyright__   = "Copyright 2014, Mikros Image"


from PyQt4 import QtGui
# from PyQt4.QtGui import QDialog
from pulitools.common import XLogger



class StandardIconDialog(QtGui.QDialog):
    '''
    '''
    
    def __init__(self, parent):

        super(self.__class__, self).__init__(parent)
        self.initUi()

    def initUi(self):

        ''' init user interface at startup
        '''
        all_icons=[
            (QtGui.QStyle.SP_TitleBarMinButton,     "SP_TitleBarMinButton"),
            (QtGui.QStyle.SP_TitleBarMenuButton,    "SP_TitleBarMenuButton"),
            (QtGui.QStyle.SP_TitleBarMaxButton,     "SP_TitleBarMaxButton"),
            (QtGui.QStyle.SP_TitleBarCloseButton,   "SP_TitleBarCloseButton"),
            (QtGui.QStyle.SP_TitleBarNormalButton,  "SP_TitleBarNormalButton"),
            (QtGui.QStyle.SP_TitleBarShadeButton,   "SP_TitleBarShadeButton"),
            (QtGui.QStyle.SP_TitleBarUnshadeButton, "SP_TitleBarUnshadeButton"),
            (QtGui.QStyle.SP_TitleBarContextHelpButton, "SP_TitleBarContextHelpButton"),
            (QtGui.QStyle.SP_MessageBoxInformation, "SP_MessageBoxInformation"),
            (QtGui.QStyle.SP_MessageBoxWarning,     "SP_MessageBoxWarning"),
            (QtGui.QStyle.SP_MessageBoxCritical,    "SP_MessageBoxCritical"),
            (QtGui.QStyle.SP_MessageBoxQuestion,    "SP_MessageBoxQuestion"),
            (QtGui.QStyle.SP_DesktopIcon,           "SP_DesktopIcon"),
            (QtGui.QStyle.SP_TrashIcon,             "SP_TrashIcon"),
            (QtGui.QStyle.SP_ComputerIcon,          "SP_ComputerIcon"),
            (QtGui.QStyle.SP_DriveFDIcon,           "SP_DriveFDIcon"),
            (QtGui.QStyle.SP_DriveHDIcon,           "SP_DriveHDIcon"),
            (QtGui.QStyle.SP_DriveCDIcon,           "SP_DriveCDIcon"),
            (QtGui.QStyle.SP_DriveDVDIcon,          "SP_DriveDVDIcon"),
            (QtGui.QStyle.SP_DriveNetIcon,          "SP_DriveNetIcon"),
            (QtGui.QStyle.SP_DirHomeIcon,           "SP_DirHomeIcon"),
            (QtGui.QStyle.SP_DirOpenIcon,           "SP_DirOpenIcon"),
            (QtGui.QStyle.SP_DirClosedIcon,         "SP_DirClosedIcon"),
            (QtGui.QStyle.SP_DirIcon,               "SP_DirIcon"),
            (QtGui.QStyle.SP_DirLinkIcon,           "SP_DirLinkIcon"),
            (QtGui.QStyle.SP_FileIcon,              "SP_FileIcon"),
            (QtGui.QStyle.SP_FileLinkIcon,          "SP_FileLinkIcon"),
            (QtGui.QStyle.SP_FileLinkIcon,          "SP_FileLinkIcon"),
            (QtGui.QStyle.SP_FileDialogEnd,         "SP_FileDialogEnd"),
            (QtGui.QStyle.SP_FileDialogToParent,        "SP_FileDialogToParent"),
            (QtGui.QStyle.SP_FileDialogNewFolder,       "SP_FileDialogNewFolder"),
            (QtGui.QStyle.SP_FileDialogDetailedView,    "SP_FileDialogDetailedView"),
            (QtGui.QStyle.SP_FileDialogInfoView,        "SP_FileDialogInfoView"),
            (QtGui.QStyle.SP_FileDialogContentsView,    "SP_FileDialogContentsView"),
            (QtGui.QStyle.SP_FileDialogListView,        "SP_FileDialogListView"),
            (QtGui.QStyle.SP_FileDialogBack,            "SP_FileDialogBack"),
            (QtGui.QStyle.SP_DockWidgetCloseButton,     "SP_DockWidgetCloseButton"),
            (QtGui.QStyle.SP_ToolBarHorizontalExtensionButton,  "SP_ToolBarHorizontalExtensionButton"),
            (QtGui.QStyle.SP_ToolBarVerticalExtensionButton,    "SP_ToolBarVerticalExtensionButton"),
            (QtGui.QStyle.SP_DialogOkButton,        "SP_DialogOkButton"),
            (QtGui.QStyle.SP_DialogCancelButton,    "SP_DialogCancelButton"),
            (QtGui.QStyle.SP_DialogHelpButton,      "SP_DialogHelpButton"),
            (QtGui.QStyle.SP_DialogOpenButton,      "SP_DialogOpenButton"),
            (QtGui.QStyle.SP_DialogSaveButton,      "SP_DialogSaveButton"),
            (QtGui.QStyle.SP_DialogCloseButton,     "SP_DialogCloseButton"),
            (QtGui.QStyle.SP_DialogApplyButton,     "SP_DialogApplyButton"),
            (QtGui.QStyle.SP_DialogResetButton,     "SP_DialogResetButton"),
            (QtGui.QStyle.SP_DialogDiscardButton,   "SP_DialogDiscardButton"),
            (QtGui.QStyle.SP_DialogYesButton,       "SP_DialogYesButton"),
            (QtGui.QStyle.SP_DialogNoButton,        "SP_DialogNoButton"),
            (QtGui.QStyle.SP_ArrowUp,               "SP_ArrowUp"),
            (QtGui.QStyle.SP_ArrowDown,             "SP_ArrowDown"),
            (QtGui.QStyle.SP_ArrowLeft,             "SP_ArrowLeft"),
            (QtGui.QStyle.SP_ArrowRight,            "SP_ArrowRight"),
            (QtGui.QStyle.SP_ArrowBack,             "SP_ArrowBack"),
            (QtGui.QStyle.SP_ArrowForward,          "SP_ArrowForward"),
            (QtGui.QStyle.SP_CommandLink,           "SP_CommandLink"),
            (QtGui.QStyle.SP_VistaShield,           "SP_VistaShield"),
            (QtGui.QStyle.SP_BrowserReload,         "SP_BrowserReload"),
            (QtGui.QStyle.SP_BrowserStop,           "SP_BrowserStop"),
            (QtGui.QStyle.SP_MediaPlay,             "SP_MediaPlay"),
            (QtGui.QStyle.SP_MediaStop,             "SP_MediaStop"),
            (QtGui.QStyle.SP_MediaPause,            "SP_MediaPause"),
            (QtGui.QStyle.SP_MediaSkipForward,      "SP_MediaSkipForward"),
            (QtGui.QStyle.SP_MediaSkipBackward,     "SP_MediaSkipBackward"),
            (QtGui.QStyle.SP_MediaSeekForward,      "SP_MediaSeekForward"),
            (QtGui.QStyle.SP_MediaSeekBackward,     "SP_MediaSeekBackward"),
            (QtGui.QStyle.SP_MediaVolume,           "SP_MediaVolume"),
            (QtGui.QStyle.SP_MediaVolumeMuted,      "SP_MediaVolumeMuted"),
        ]

        self.layout = QtGui.QVBoxLayout()
        self.setLayout( self.layout );
        self.setWindowTitle('Standard icons')

        self.list = QtGui.QListWidget( self );
        self.layout.addWidget( self.list );

        for iconId, iconName in all_icons:
            icon = self.style().standardIcon( iconId )
            self.list.addItem( QtGui.QListWidgetItem(icon, iconName, self.list, 0) )


    def closeEvent(self, event):
        # update app settings 
        XLogger().debug("Close StandardIconDialog")
        pass