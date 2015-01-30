from PyQt4.QtCore import Qt
from PyQt4.QtGui import QAbstractItemView, QMenu, QCursor, QTreeView

from pulimonitor.ui.headerview import HeaderView
from pulimonitor.ui.rendernode.model import RN_COL_INIT_WIDTH


class JobHeaderView(HeaderView):
    '''
    Subclass re-implementing the necessary methods to for the additional
    functionality from HeaderView.
    '''

    def sectionSizes(self):
        return RN_COL_INIT_WIDTH

    def sectionResizeModes(self):
        return HeaderView.sectionResizeModes(self)

    def sectionHiddenStatus(self):
        return HeaderView.sectionHiddenStatus(self)


class JobTreeView(QTreeView):
    '''
    Subclass providing a context menu and custom settings for the job tree view.
    '''

    def __init__(self, parent=None):
        super(JobTreeView, self).__init__(parent)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setSortingEnabled(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setHeader(JobHeaderView(Qt.Horizontal))
        self.header().setColumnsHidable(True)
        self.header().setMovable(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.onContextMenu)

    def onContextMenu(self, pos):
        menu = QMenu(self)
        menu.addActions(self.actions())
        menu.exec_(QCursor.pos())
