from PyQt4.QtCore import Qt
from PyQt4.QtGui import QWidget, QVBoxLayout, QHBoxLayout

from ui.action import Action
from ui.rendernode.details import RenderNodeDetails
from ui.rendernode.model import RenderNodeTableProxyModel
from ui.rendernode.view import RenderNodeTableView
from ui.searchlineedit import SearchLineEdit
from util.user import currentUser


class RenderNodePanel(QWidget):

    def __init__(self, parent):
        super(RenderNodePanel, self).__init__(parent)
        self.mainLayout = QVBoxLayout(self)
        self.searchLineEdit = SearchLineEdit(self)
        searchLayout = QHBoxLayout()
        searchLayout.addWidget(self.searchLineEdit)
        self.tableView = RenderNodeTableView(self)
        self.tableModel = RenderNodeTableProxyModel(self)
        self.searchLineEdit.setModel(self.tableModel)
        self.tableView.setModel(self.tableModel)
        self.mainLayout.addLayout(searchLayout)
        self.mainLayout.addWidget(self.tableView)
        self.renderNodeDetails = RenderNodeDetails(self)
        self.mainLayout.addWidget(self.renderNodeDetails)
        self.tableView.selectionModel().selectionChanged.connect(self._selectionChanged)
        self.setupActions()

    def onDataUpdate(self, data):
        '''
        This slot is called once there is new data available for this panel.
        The data is then propagated to the widgets, which decide on how to
        actually use it.
        :param data: a list of rendernode data entities
        :type data: list
        '''
        self.tableModel.onDataUpdate(data)

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
        print "pause clicked"

    def setupActions(self):
        '''
        Setup all Actions this panel provides.
        '''

        a = Action("Pause/Resume", self)
        a.category = "Rendernode"
        a.id = 1
        a.triggered.connect(self.onPauseAction)
        self.addAction(a)
        self.tableView.addAction(a)
        a.setEnabled(a.id in currentUser().allowedActions())
#         Action("Restart")
#         Action("Kill and Pause")
#         Action("Kill and Restart")
#         Action("Quarantine")
#         Action("Unquarantine")
#         Action("Delete")
#         Action("Show Log")
#         Action("Open XTerm")
#         Action("Open VNC")
#         Action("Remove Pools")
