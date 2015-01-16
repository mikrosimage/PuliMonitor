'''
Main module setting up logging, required dependencies, api versions and the
actual application.
'''

import sys

# setup logger
from util import logger
logger.setupConsoleLogger()
logger.setupFileLogger()

# test requirements
from util import requirements
if not requirements.fulfilled():
    sys.exit(1)

# set sip api v2 needs to be done before importing anything Qt related
from ui.qthelpers import setSipApiVersion
setSipApiVersion(2)

from PyQt4.QtGui import QApplication, QIcon

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

# prompt for login
login = LoginDialog()
if not login.exec_():
    sys.exit(1)
mainwindow = MainWindow()
mainwindow.show()
returnCode = app.exec_()
sys.exit(returnCode)
