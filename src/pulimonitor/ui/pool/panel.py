import logging

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QWidget, QVBoxLayout, QHBoxLayout, qApp, QMessageBox

from pulimonitor.ui.action import Action
from pulimonitor.ui.pool.edit import PoolEditDialog
from pulimonitor.ui.pool.model import PoolTableProxyModel, PoolTableModel
from pulimonitor.ui.pool.view import PoolTableView
from pulimonitor.ui.searchlineedit import SearchLineEdit
from pulimonitor.network.requesthandler import getRequestHandler


class PoolPanel(QWidget):

    sourceModel = None

    def __init__(self, parent=None):
        super(PoolPanel, self).__init__(parent)
        self.log = logging.getLogger(__name__)
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setSpacing(2)
        self.searchLineEdit = SearchLineEdit(self)
        searchLayout = QHBoxLayout()
        searchLayout.addWidget(self.searchLineEdit)
        self.tableView = PoolTableView(self)
        if PoolPanel.sourceModel is None:
            PoolPanel.sourceModel = PoolTableModel(qApp)
        self.tableModel = PoolTableProxyModel(PoolPanel.sourceModel, self)
        self.searchLineEdit.setModel(self.tableModel)
        self.tableView.setModel(self.tableModel)
        self.mainLayout.addLayout(searchLayout)
        self.mainLayout.addWidget(self.tableView)
        self.setupActions()

    def __addAction(self, text, aId, selectionSensitive):
        a = Action(text, "Pools", aId, selectionSensitive, self)
        self.addAction(a)
        self.tableView.addAction(a)
        return a

    def onAddPool(self):
        d = PoolEditDialog("", self)
        d.exec_()

    def onDeletePool(self):
        poolsToDelete = []
        for index in self.tableView.selectionModel().selectedRows():
            rowData = index.data(Qt.UserRole)
            poolsToDelete.append(rowData.get("name"))
        choice = QMessageBox.question(self, "Delete?", "Are you sure you want"
                                      "to delete the pools:\n" + "\n".join(poolsToDelete),
                                      buttons=QMessageBox.Yes | QMessageBox.No,
                                      defaultButton=QMessageBox.No)
        if choice == QMessageBox.Yes:
            rh = getRequestHandler()
            for pool in poolsToDelete:
                if not rh.deletePool(pool):
                    QMessageBox.critical(self, "Error", "Deleting pool %s failed!" % (pool))

    def setupActions(self):
        '''
        Setup all Actions this panel provides.
        '''
        a = self.__addAction("Add", 110, False)
        a.triggered.connect(self.onAddPool)
        a = self.__addAction("Delete", 111, True)
        a.triggered.connect(self.onDeletePool)
#         a = self.__addAction("Pause/Resume", 100)
#         a.triggered.connect(self.onPauseAction)
#         a = self.__addAction("Restart", 101)
# #         a.triggered.connect(self.onPauseAction)
#         a = self.__addAction("Kill and Pause", 102)
# #         a.triggered.connect(self.onPauseAction)
#         a = self.__addAction("Kill and Restart", 103)
# #         a.triggered.connect(self.onPauseAction)
#         a = self.__addAction("Quarantine", 104)
# #         a.triggered.connect(self.onPauseAction)
#         a = self.__addAction("Unquarantine", 105)
# #         a.triggered.connect(self.onPauseAction)
#         a = self.__addAction("Delete", 106)
# #         a.triggered.connect(self.onPauseAction)
#         a = self.__addAction("Show Log", 107)
# #         a.triggered.connect(self.onPauseAction)
#         a = self.__addAction("Open XTerm", 108)
#         a.triggered.connect(self.onXTermAction)
#         a = self.__addAction("Open VNC", 109)
#         a.triggered.connect(self.onVncAction)
