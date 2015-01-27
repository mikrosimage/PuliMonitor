import logging

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QWidget, QVBoxLayout, QHBoxLayout, qApp

from ui.action import Action
from ui.job.details import JobDetails
from ui.job.model import JobTreeProxyModel, JobTreeModel
from ui.job.view import JobTreeView
from ui.searchlineedit import SearchLineEdit


class JobPanel(QWidget):

    sourceModel = None

    def __init__(self, parent=None):
        super(JobPanel, self).__init__(parent)
        self.log = logging.getLogger(__name__)
        self.mainLayout = QVBoxLayout(self)
        self.searchLineEdit = SearchLineEdit(self)
        searchLayout = QHBoxLayout()
        searchLayout.addWidget(self.searchLineEdit)
        self.treeView = JobTreeView(self)
        if JobPanel.sourceModel is None:
            JobPanel.sourceModel = JobTreeModel(qApp)
        self.treeModel = JobTreeProxyModel(JobPanel.sourceModel, self)
        self.searchLineEdit.setModel(self.treeModel)
        self.treeView.setModel(self.treeModel)
        self.mainLayout.addLayout(searchLayout)
        self.mainLayout.addWidget(self.treeView)
        self.jobDetails = JobDetails(self)
        self.mainLayout.addWidget(self.jobDetails)
        self.treeView.selectionModel().selectionChanged.connect(self._selectionChanged)
        self.setupActions()

    def _selectionChanged(self, selected, deselected):
        '''
        Slot called when the tree view selection changes, notifying dependent
        widgets.
        :param selected: selected items
        :type selected: QItemSelection
        :param deselected: deselected items
        :type deselected: QItemSelection
        '''
        for index in selected.indexes():
            self.jobDetails.refresh(index.data(Qt.UserRole))
            return

    def __addAction(self, text, aId):
        a = Action(text, "Jobs", aId, self)
        self.addAction(a)
        self.treeView.addAction(a)
        return a

    def onPauseAction(self):
        pass

    def setupActions(self):
        '''
        Setup all Actions this panel provides.
        '''
        a = self.__addAction("Pause", 1)
        a.triggered.connect(self.onPauseAction)
