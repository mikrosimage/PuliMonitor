from PyQt4.QtCore import QSettings

from pulimonitor.util.path import GENERAL_CONFIG_PATH


class Config(QSettings):
    '''
    QSettings subclass that allows to conveniently access/write settings.
    '''

    def __init__(self, parent=None):
        QSettings.__init__(self, GENERAL_CONFIG_PATH, QSettings.IniFormat, parent)

        self.servers = []
        self.beginGroup("Servers")
        keys = self.allKeys()
        for k in keys:
            hostname, port = self.value(k).split(":")
            self.servers.append((hostname, int(port)))
        self.endGroup()

        self.beginGroup("General")
        self.refreshInterval = self.value("refresh_interval", 3, int) * 1000
        self.endGroup()

        self.beginGroup("VNC")
        self.vncCommand = self.value("vnc_command", "vncviewer {hostname}", str)
        self.endGroup()


if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import QApplication
    app = QApplication([])
    c = Config()
    sys.exit(app.exec_())
