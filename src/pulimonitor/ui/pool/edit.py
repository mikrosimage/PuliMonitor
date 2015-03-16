'''
Created on Feb 2, 2015

@author: sebels
'''

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QDialog, QLineEdit, QVBoxLayout, QDialogButtonBox, \
    QFormLayout

from pulimonitor.network import requesthandler


class PoolEditDialog(QDialog):

    def __init__(self, pool, parent=None):
        super(PoolEditDialog, self).__init__(parent)
        self.mainLayout = QVBoxLayout(self)
        self.formLayout = QFormLayout()
        self.nameLineEdit = QLineEdit(self)
        self.formLayout.addRow("Name:", self.nameLineEdit)
        self.mainLayout.addLayout(self.formLayout)
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
                                          Qt.Horizontal, self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.mainLayout.addWidget(self.buttonBox)

    def accept(self, *args, **kwargs):
        name = self.nameLineEdit.text()
        if name:
            rh = requesthandler.get()
            rh.addPool(name)
        return QDialog.accept(self, *args, **kwargs)

    def reject(self, *args, **kwargs):
        return QDialog.reject(self, *args, **kwargs)


def main():
    import sys
    from PyQt4.QtGui import QApplication
    app = QApplication([])
    w = PoolEditDialog()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
