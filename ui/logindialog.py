import getpass

from PyQt4.QtCore import QSettings, QByteArray
from PyQt4.QtGui import QDialog, QVBoxLayout, QFormLayout, \
    QLabel, QLineEdit, QDialogButtonBox, QApplication

from util import user


def userIsValid(username, password):
    '''
    Check if the user is valid.
    :param username: username to check
    :type username: str
    :param password: password to check (unencrypted)
    :type password: str
    '''

    return True


class LoginDialog(QDialog):

    def __init__(self, parent=None):
        """
        Login dialog asks users for name and password. It will also create a
        User object and register it globally, so every module can access it
        via user.currentUser()
        """
        QDialog.__init__(self, parent)
        settings = QSettings()
        settings.beginGroup(self.__class__.__name__)
        self.restoreGeometry(settings.value("geometry", QByteArray()))
        settings.endGroup()

        self.setWindowTitle("Login")
        self.verticalLayout = QVBoxLayout(self)
        self.formLayout = QFormLayout()

        self.usernameLineEdit = QLineEdit(self)
        self.usernameLineEdit.setText(getpass.getuser())
        self.formLayout.addRow("Username:", self.usernameLineEdit)

        self.passwordLineEdit = QLineEdit(self)
        self.formLayout.addRow("Password:", self.passwordLineEdit)
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)

        self.verticalLayout.addLayout(self.formLayout)
        self.statusLabel = QLabel(self)
        self.statusLabel.setText("")
        self.verticalLayout.addWidget(self.statusLabel)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.verticalLayout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.setTabOrder(self.usernameLineEdit, self.passwordLineEdit)
        self.setTabOrder(self.passwordLineEdit, self.buttonBox)

    def accept(self):
        """
        Called when clicked on OK or Cancel
        """
        # TODO: a backend needs to be plugged in here to actually check the user data against
        username = self.usernameLineEdit.text()
        password = self.passwordLineEdit.text()
        if userIsValid(username, password):
            user.loginUser(username)
            settings = QSettings()
            settings.beginGroup(self.__class__.__name__)
            settings.setValue("geometry", self.saveGeometry())
            settings.endGroup()
            QDialog.accept(self)
        else:
            self.statusLabel.setText("Incorrect login!")


def main():
    import sys
    app = QApplication([])
    w = LoginDialog()
    w.exec_()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
