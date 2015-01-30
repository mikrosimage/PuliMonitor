from PyQt4.Qt import PYQT_VERSION_STR
from PyQt4.QtCore import QT_VERSION_STR
from PyQt4.QtGui import QMessageBox
from sip import SIP_VERSION_STR


APP_NAME = "PuliMonitor"
APP_VERSION = 0.1


def dialog(self):
    '''
    Basic about dialog with version information of the current
    '''

    msg = '''
    <h3>{APP_NAME}</h3>
    <span>v{APP_VERSION}</span>
    <h4>Dependencies</h4>
    <table>
    <tr><td>Qt</td><td>{qtVersion}</td></tr>
    <tr><td>PyQt</td><td>{pyqtVersion}</td></tr>
    <tr><td>Sip</td><td>{sipVersion}</td></tr>
    </table>
    '''.format(APP_NAME=APP_NAME, APP_VERSION=APP_VERSION, qtVersion=QT_VERSION_STR,
               pyqtVersion=PYQT_VERSION_STR, sipVersion=SIP_VERSION_STR)
    QMessageBox.about(None, 'About %s' % APP_NAME, msg)
