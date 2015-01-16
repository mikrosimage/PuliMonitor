'''
This module allows the installation of an exception hook, which will catch
any unexpected exception and log it to the root logger. Additionally it can
display a QMessageBox and shut down the application, so users don't continue
using a broken application
'''

import logging
import sys
import traceback

from PyQt4.QtGui import QApplication, QMessageBox


def handleException(exceptionType, exceptionValue, exceptionTraceback):
    '''
    Handles an exception logging it to the root logger. Arguments are equal to
    sys.excepthook()
    '''
    logger = logging.getLogger("")
    tb = "".join(traceback.format_exception(exceptionType, exceptionValue,
                                            exceptionTraceback))
    logger.exception("\n" + tb)


def handleExceptionQt(exceptionType, exceptionValue, exceptionTraceback):
    '''
    Handles an exception by first logging it and then showing a QMessageBox
    with an error message. The QApplication is then exited. Arguments are equal
    to sys.excepthool()
    '''

    handleException(exceptionType, exceptionValue, exceptionTraceback)
    msg = QMessageBox()
    msg.setWindowTitle("Error")
    msg.setText("There was an unexpected error. Please check your log files. "
                "The application will closed now.")
    msg.setIcon(QMessageBox.Critical)
    msg.setDetailedText(exceptionValue.message)
    msg.exec_()
    app = QApplication.instance()
    app.quit()


# re-wire original hook
def install():
    sys.excepthook = handleException
