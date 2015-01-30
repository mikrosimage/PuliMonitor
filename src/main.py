'''
Main module setting up logging, required dependencies, api versions and the
actual application.
'''

import logging.config
import sys

# setting the sip api to v2 needs to be done before importing anything Qt related
# things, so we put it first
from pulimonitor.ui.sipapi import setVersion
setVersion(2)

from PyQt4.QtGui import QApplication, QIcon, QMessageBox

from pulimonitor.network.utils import testConnectivity
from pulimonitor.ui.about import APP_NAME
from pulimonitor.ui.logindialog import LoginDialog
from pulimonitor.ui.mainwindow import MainWindow
from pulimonitor.ui.palette import standardPalette
from pulimonitor.util import exceptionhook
from pulimonitor.util import requirements
from pulimonitor.util.path import LOG_CONFIG_PATH


def main():
    # setup logging first
    logging.config.fileConfig(LOG_CONFIG_PATH)

    # test requirements
    if not requirements.fulfilled():
        sys.exit(1)

    # install the exception hook to catch and log all exception
    exceptionhook.install()

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


if __name__ == '__main__':
    main()
