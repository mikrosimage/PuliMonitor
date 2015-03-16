import logging
import subprocess

from PyQt4.QtGui import QWidget, QVBoxLayout, QHBoxLayout, QMessageBox, qApp, \
    QErrorMessage

from pulimonitor.network.requesthandler import RequestHandler
from pulimonitor.ui.action import Action
from pulimonitor.ui.rendernode.stats import RenderNodeStatsWidget
from pulimonitor.ui.rendernode.treemodel import RenderNodeModel, \
    RenderNodeProxyModel
from pulimonitor.ui.rendernode.treeview import RenderNodeTreeView
from pulimonitor.ui.searchlineedit import SearchLineEdit
from pulimonitor.util import config
from pulimonitor.util.user import currentUser


class RenderNodePanel(QWidget):

    sourceModel = None

    def __init__(self, parent=None):
        super(RenderNodePanel, self).__init__(parent)
        self.log = logging.getLogger(__name__)
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setSpacing(2)
        self.searchLineEdit = SearchLineEdit(self)
        searchLayout = QHBoxLayout()
        searchLayout.addWidget(self.searchLineEdit)
        self.treeView = RenderNodeTreeView(self)
        self.statsWidget = RenderNodeStatsWidget(self)
        if RenderNodePanel.sourceModel is None:
            RenderNodePanel.sourceModel = RenderNodeModel(qApp)
        self.treeModel = RenderNodeProxyModel(RenderNodePanel.sourceModel, self)
        self.searchLineEdit.setModel(self.treeModel)
        self.treeView.setModel(self.treeModel)
        self.mainLayout.addLayout(searchLayout)
        self.mainLayout.addWidget(self.treeView)
        self.mainLayout.addWidget(self.statsWidget)
        self.setupActions()

    def onPauseAction(self):
        '''
        Slot called once the pause action is triggered
        '''
        rendernodes = self.treeView.selectedRenderNodes()
        rh = RequestHandler()
        erroneous = rh.setRenderNodesPaused(rendernodes, True, False)
        if erroneous:
            QErrorMessage(self).showMessage("Error unpausing: %s" % ("\n".join(erroneous)))

    def onUnpauseAction(self):
        '''
        Slot called once the pause action is triggered
        '''
        rendernodes = self.treeView.selectedRenderNodes()
        rh = RequestHandler()
        erroneous = rh.setRenderNodesPaused(rendernodes, False, False)
        if erroneous:
            QErrorMessage(self).showMessage("Error unpausing: %s" % ("\n".join(erroneous)))

    def onTerminalOpenAction(self):
        '''
        Slot called on the "Open Terminal" action is triggered.
        '''
        cmdTemplate = config.get().get("SSH-Terminal", "ssh_command")
        for rn in self.treeView.selectedRenderNodes():
            cu = currentUser().name
            sshCommand = cmdTemplate.format(user=cu, host=rn.host)
            try:
                self.log.debug("opening terminal with command: " + sshCommand)
                subprocess.Popen(sshCommand, shell=True)
            except:
                msg = "Could not open terminal."
                self.log.exception(msg)
                QMessageBox.critical(None, "Error", msg)

    def onVncAction(self):
        '''
        Slot called once the Show VNC action is triggered.
        '''
        cmdTemplate = config.get().get("VNC", "vnc_command")
        for rn in self.treeView.selectedRenderNodes():
            vncCommand = cmdTemplate.format(hostname=rn.host)
            self.log.debug("opening vnc with command: {0}".format(vncCommand))
            try:
                subprocess.Popen(vncCommand, shell=True)
            except:
                msg = "Could not open VNC with command: {0}".format(vncCommand)
                self.log.exception(msg)
                QMessageBox.critical(None, "Error", msg)

    def __addAction(self, text, aId, selectionSensitive):
        a = Action(text, "Rendernode", aId, selectionSensitive, self)
        self.addAction(a)
        self.treeView.addAction(a)
        return a

    def setupActions(self):
        '''
        Setup all Actions this panel provides.
        '''
        a = self.__addAction("Pause", 1, True)
        a.triggered.connect(self.onPauseAction)
        a = self.__addAction("Unpause", 12, True)
        a.triggered.connect(self.onUnpauseAction)
        a = self.__addAction("Restart", 2, True)
#         a.triggered.connect(self.onPauseAction)
        a = self.__addAction("Kill and Pause", 3, True)
#         a.triggered.connect(self.onPauseAction)
        a = self.__addAction("Kill and Restart", 4, True)
#         a.triggered.connect(self.onPauseAction)
        a = self.__addAction("Quarantine", 5, True)
#         a.triggered.connect(self.onPauseAction)
        a = self.__addAction("Unquarantine", 6, True)
#         a.triggered.connect(self.onPauseAction)
        a = self.__addAction("Delete", 7, True)
#         a.triggered.connect(self.onPauseAction)
        a = self.__addAction("Show Log", 8, True)
#         a.triggered.connect(self.onPauseAction)
        a = self.__addAction("Open Terminal", 9, True)
        a.triggered.connect(self.onTerminalOpenAction)
        a = self.__addAction("Open VNC", 10, True)
        a.triggered.connect(self.onVncAction)
        a = self.__addAction("Remove Pools", 11, True)
#         a.triggered.connect(self.onPauseAction)
