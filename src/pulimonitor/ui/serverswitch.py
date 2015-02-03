'''
Created on Feb 2, 2015

@author: sebels
'''

from PyQt4.QtCore import Qt, pyqtSignal
from PyQt4.QtGui import QDialog, QVBoxLayout, QDialogButtonBox, \
    QFormLayout

from pulimonitor.network.requesthandler import getRequestHandler
from pulimonitor.ui.combobox import ComboBox


class ServerSwitchDialog(QDialog):

    serverChanged = pyqtSignal(tuple)

    def __init__(self, parent=None):
        super(ServerSwitchDialog, self).__init__(parent)
        self.mainLayout = QVBoxLayout(self)
        self.formLayout = QFormLayout()
        self.serverComboBox = ComboBox(self)
        self.formLayout.addRow("Server:", self.serverComboBox)
        self.mainLayout.addLayout(self.formLayout)
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
                                          Qt.Horizontal, self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.mainLayout.addWidget(self.buttonBox)
        self.addServers()
        self.serverComboBox.currentItemChanged.connect(self.serverChanged.emit)

    def addServers(self):
        rh = getRequestHandler()
        for hostname, port in rh.serversOnline:
            self.serverComboBox.addItem(hostname, (hostname, port))

    def onCurrentServerChanged(self, data):
        idx = self.serverComboBox.currentIndex()
        data = self.serverComboBox.itemData(idx)
        return data


def main():
    import sys
    from PyQt4.QtGui import QApplication
    app = QApplication([])
    w = ServerSwitchDialog()
    w.addServers()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
