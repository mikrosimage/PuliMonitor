from PyQt4.QtCore import Qt
from PyQt4.QtGui import QAbstractItemView, QMenu, QCursor

from pulimonitor.ui.headerview import HeaderView
from pulimonitor.ui.pool.model import COL_INIT_WIDTH
from pulimonitor.ui.tableview import TableView


class PoolHeaderView(HeaderView):
    '''
    Subclass re-implementing the necessary methods to for the additional
    functionality from HeaderView.
    '''

    def __init__(self, orientation, parent=None):
        super(PoolHeaderView, self).__init__(orientation, parent)
        self.setClickable(True)

    def sectionSizes(self):
        return COL_INIT_WIDTH

    def sectionResizeModes(self):
        return HeaderView.sectionResizeModes(self)

    def sectionHiddenStatus(self):
        return HeaderView.sectionHiddenStatus(self)


class PoolTableView(TableView):
    '''
    Subclass providing a context menu and custom settings for the pools table view.
    '''

    def __init__(self, parent=None):
        super(PoolTableView, self).__init__(parent)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setShowGrid(False)
        self.setHorizontalHeader(PoolHeaderView(Qt.Horizontal))
        self.horizontalHeader().setColumnsHidable(True)
        self.horizontalHeader().setMovable(True)
        self.verticalHeader().setVisible(False)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.onContextMenu)

    def onContextMenu(self, pos):
        menu = QMenu(self)
        menu.addActions(self.actions())
        menu.exec_(QCursor.pos())
