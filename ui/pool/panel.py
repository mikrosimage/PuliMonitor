import logging

from PyQt4.QtGui import QWidget, QVBoxLayout, QHBoxLayout, qApp

from ui.action import Action
from ui.pool.model import PoolTableProxyModel, PoolTableModel
from ui.pool.view import PoolTableView
from ui.searchlineedit import SearchLineEdit


class PoolPanel(QWidget):

    sourceModel = None

    def __init__(self, parent=None):
        super(PoolPanel, self).__init__(parent)
        self.log = logging.getLogger(__name__)
        self.mainLayout = QVBoxLayout(self)
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

    def onPauseAction(self):
        '''
        Slot called once the pause action is triggered
        '''
        print "pause clicked"

    def __addAction(self, text, aId):
        a = Action(text, "Pools", aId, self)
        self.addAction(a)
        self.tableView.addAction(a)
        return a

    def onXTermAction(self):
        '''
        Slot called once the XTerm action is triggered.
        '''
        pass

    def onVncAction(self):
        '''
        Slot called once the Show VNC action is triggered.
        '''
        pass

    def setupActions(self):
        '''
        Setup all Actions this panel provides.
        '''
        a = self.__addAction("Pause/Resume", 100)
        a.triggered.connect(self.onPauseAction)
        a = self.__addAction("Restart", 101)
#         a.triggered.connect(self.onPauseAction)
        a = self.__addAction("Kill and Pause", 102)
#         a.triggered.connect(self.onPauseAction)
        a = self.__addAction("Kill and Restart", 103)
#         a.triggered.connect(self.onPauseAction)
        a = self.__addAction("Quarantine", 104)
#         a.triggered.connect(self.onPauseAction)
        a = self.__addAction("Unquarantine", 105)
#         a.triggered.connect(self.onPauseAction)
        a = self.__addAction("Delete", 106)
#         a.triggered.connect(self.onPauseAction)
        a = self.__addAction("Show Log", 107)
#         a.triggered.connect(self.onPauseAction)
        a = self.__addAction("Open XTerm", 108)
        a.triggered.connect(self.onXTermAction)
        a = self.__addAction("Open VNC", 109)
        a.triggered.connect(self.onVncAction)
