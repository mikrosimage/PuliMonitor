import os
import sys

from PyQt4.QtCore import QSettings
from PyQt4.QtGui import QApplication


class Config(QSettings):
    '''
    QSettings subclass that allows to conveniently access/write settings.
    '''

    def __init__(self, parent=None):
        configFilePath = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "settings.ini")
        QSettings.__init__(self, configFilePath, QSettings.IniFormat, parent)

        self.beginGroup("Server")
        self.hostname = self.value("hostname", "localhost", str)
        self.port = self.value("port", 8004, int)
        self.endGroup()

        self.beginGroup("General")
        self.refreshInterval = self.value("refresh_interval", 3, int) * 1000
        self.endGroup()

        self.beginGroup("VNC")
        self.vncCommand = self.value("vnc_command", "vncviewer {hostname}", str)
        self.endGroup()


if __name__ == '__main__':
    import sys
    app = QApplication([])
    c = Config()
    print c.hostname
    sys.exit(app.exec_())
