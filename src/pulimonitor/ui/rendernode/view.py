from PyQt4.QtCore import Qt
from PyQt4.QtGui import QAbstractItemView, QMenu, QCursor

from pulimonitor.ui.headerview import HeaderView
from pulimonitor.ui.progressbardelegate import ProgressBarDelegate
from pulimonitor.ui.rendernode.model import RN_COL_INIT_WIDTH, RN_COL_NAMES
from pulimonitor.ui.tableview import TableView


class RenderNodeHeaderView(HeaderView):
    '''
    Subclass re-implementing the necessary methods to for the additional
    functionality from HeaderView.
    '''

    def __init__(self, orientation, parent=None):
        super(RenderNodeHeaderView, self).__init__(orientation, parent)
        self.setClickable(True)

    def sectionSizes(self):
        return RN_COL_INIT_WIDTH

    def sectionResizeModes(self):
        return HeaderView.sectionResizeModes(self)

    def sectionHiddenStatus(self):
        return HeaderView.sectionHiddenStatus(self)


class RenderNodeTableView(TableView):
    '''
    Subclass providing a context menu and custom settings for the render nodes
    table view.
    '''

    def __init__(self, parent=None):
        super(RenderNodeTableView, self).__init__(parent)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setShowGrid(False)
        self.setHorizontalHeader(RenderNodeHeaderView(Qt.Horizontal))
        self.horizontalHeader().setColumnsHidable(True)
        self.horizontalHeader().setMovable(True)
        self.verticalHeader().setVisible(False)
        self.setItemDelegateForColumn(RN_COL_NAMES.index("RAM Usage"), ProgressBarDelegate())
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.onContextMenu)

    def onContextMenu(self, pos):
        menu = QMenu(self)
        menu.addActions(self.actions())
        menu.exec_(QCursor.pos())
