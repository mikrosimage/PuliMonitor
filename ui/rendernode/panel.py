import json
import logging
import subprocess

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QWidget, QVBoxLayout, QHBoxLayout, QMessageBox, qApp
import requests

from network.requesthandler import getRequestHandler
from ui.action import Action
from ui.rendernode.details import RenderNodeDetails
from ui.rendernode.model import RenderNodeTableProxyModel, RenderNodeTableModel
from ui.rendernode.stats import RenderNodeStatsWidget
from ui.rendernode.view import RenderNodeTableView
from ui.searchlineedit import SearchLineEdit
from util.config import Config
from util.user import currentUser


class RenderNodePanel(QWidget):

    sourceModel = None

    def __init__(self, parent=None):
        super(RenderNodePanel, self).__init__(parent)
        self.log = logging.getLogger(__name__)
        self.mainLayout = QVBoxLayout(self)
        self.searchLineEdit = SearchLineEdit(self)
        searchLayout = QHBoxLayout()
        searchLayout.addWidget(self.searchLineEdit)
        self.tableView = RenderNodeTableView(self)
        if RenderNodePanel.sourceModel is None:
            RenderNodePanel.sourceModel = RenderNodeTableModel(qApp)
        self.tableModel = RenderNodeTableProxyModel(RenderNodePanel.sourceModel, self)
        self.searchLineEdit.setModel(self.tableModel)
        self.tableView.setModel(self.tableModel)
        self.mainLayout.addLayout(searchLayout)
        self.mainLayout.addWidget(self.tableView)
        self.statsWidget = RenderNodeStatsWidget(self)
        self.mainLayout.addWidget(self.statsWidget)
        self.renderNodeDetails = RenderNodeDetails(self)
        self.mainLayout.addWidget(self.renderNodeDetails)
        self.tableView.selectionModel().selectionChanged.connect(self._selectionChanged)
        self.setupActions()

    def _selectionChanged(self, selected, deselected):
        '''
        Slot called when the render nodes view table selection changes,
        notifying dependent widgets.
        :param selected: selected items
        :type selected: QItemSelection
        :param deselected: deselected items
        :type deselected: QItemSelection
        '''
        for index in selected.indexes():
            self.renderNodeDetails.refresh(index.data(Qt.UserRole))
            return

    def onPauseAction(self):
        '''
        Slot called once the pause action is triggered
        '''
        rh = getRequestHandler()
        for index in self.tableView.selectionModel().selectedRows():
            rowData = index.data(Qt.UserRole)
            name = rowData.get("name")
            self.log.info("pausing " + name)
            r = requests.put(rh.baseUrl + "/rendernodes/{name}/paused/".format(name=name),
                             data=json.dumps({"paused": True, "killproc": False}))

    def onUnpauseAction(self):
        '''
        Slot called once the pause action is triggered
        '''
        rh = getRequestHandler()
        for index in self.tableView.selectionModel().selectedRows():
            rowData = index.data(Qt.UserRole)
            name = rowData.get("name")
            self.log.info("unpausing " + name)
            r = requests.put(rh.baseUrl + "/rendernodes/{name}/paused/".format(name=name),
                             data=json.dumps({"paused": False, "killproc": False}))

    def onXTermAction(self):
        '''
        Slot called once the XTerm action is triggered.
        '''
        for index in self.tableView.selectionModel().selectedRows():
            rowData = index.data(Qt.UserRole)
            hostname = rowData.get("host")
            cu = currentUser().name
            self.log.debug("opening xterm for user {0}@{1}".format(cu, hostname))
            try:
                subprocess.Popen(["xterm", "-e", "ssh",
                                  "{0}@{1}".format(cu, hostname)])
            except:
                msg = "Could not open xterm."
                self.log.exception(msg)
                QMessageBox.critical(None, "Error", msg)

    def onVncAction(self):
        '''
        Slot called once the Show VNC action is triggered.
        '''
        config = Config()
        for index in self.tableView.selectionModel().selectedRows():
            rowData = index.data(Qt.UserRole)
            hostname = rowData.get("host")
            vncCommand = config.vncCommand.format(hostname=hostname)
            self.log.debug("opening vnc with command: {0}".format(vncCommand))
            try:
                subprocess.Popen(vncCommand, shell=True)
            except:
                msg = "Could not open VNC with command: {0}".format(vncCommand)
                self.log.exception(msg)
                QMessageBox.critical(None, "Error", msg)

    def __addAction(self, text, aId):
        a = Action(text, "Rendernode", aId, self)
        self.addAction(a)
        self.tableView.addAction(a)
        return a

    def setupActions(self):
        '''
        Setup all Actions this panel provides.
        '''
        a = self.__addAction("Pause", 1)
        a.triggered.connect(self.onPauseAction)
        a = self.__addAction("Unpause", 12)
        a.triggered.connect(self.onUnpauseAction)
        a = self.__addAction("Restart", 2)
#         a.triggered.connect(self.onPauseAction)
        a = self.__addAction("Kill and Pause", 3)
#         a.triggered.connect(self.onPauseAction)
        a = self.__addAction("Kill and Restart", 4)
#         a.triggered.connect(self.onPauseAction)
        a = self.__addAction("Quarantine", 5)
#         a.triggered.connect(self.onPauseAction)
        a = self.__addAction("Unquarantine", 6)
#         a.triggered.connect(self.onPauseAction)
        a = self.__addAction("Delete", 7)
#         a.triggered.connect(self.onPauseAction)
        a = self.__addAction("Show Log", 8)
#         a.triggered.connect(self.onPauseAction)
        a = self.__addAction("Open XTerm", 9)
        a.triggered.connect(self.onXTermAction)
        a = self.__addAction("Open VNC", 10)
        a.triggered.connect(self.onVncAction)
        a = self.__addAction("Remove Pools", 11)
#         a.triggered.connect(self.onPauseAction)
