'''
Main module setting up logging, required dependencies, api versions and the
actual application.
'''

import sys

import logging.config

logging.config.fileConfig('logging.conf')

# test requirements
from util import requirements
if not requirements.fulfilled():
    sys.exit(1)

# set sip api v2 needs to be done before importing anything Qt related
from ui.qthelpers import setSipApiVersion
setSipApiVersion(2)

from util import exceptionhook
exceptionhook.install()

from PyQt4.QtGui import QApplication, QIcon, QMessageBox

from ui.about import APP_NAME
from ui.palette import standardPalette
from ui.mainwindow import MainWindow
from ui.logindialog import LoginDialog

# setup app
app = QApplication(sys.argv)

# set style
app.setStyle("plastique")
app.setPalette(standardPalette())
app.setWindowIcon(QIcon(":/puli.png"))

# do not change, users will loose their settings
app.setApplicationName(APP_NAME)
app.setOrganizationName("OpenRenderManagement")
app.setOrganizationDomain("opensource.mikrosimage.eu")

# Test connectivity and dont start if server is not reachable
from network.utils import testConnectivity
if not testConnectivity():
    QMessageBox.critical(None, "Error", "Connecting to the server defined in "
                         "settings.ini failed!")
    app.exit(1)
    sys.exit(1)

# prompt for login
login = LoginDialog()
if not login.exec_():
    app.exit(1)
    sys.exit(1)
mainwindow = MainWindow()
mainwindow.show()
returnCode = app.exec_()
sys.exit(returnCode)
