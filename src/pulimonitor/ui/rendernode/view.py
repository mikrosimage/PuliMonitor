from PyQt4.QtCore import Qt, pyqtSignal
from PyQt4.QtGui import QAbstractItemView, QMenu, QCursor

from pulimonitor.ui.checkboxdelegate import CheckBoxDelegate
from pulimonitor.ui.headerview import HeaderView
from pulimonitor.ui.progressbardelegate import ProgressBarDelegate
from pulimonitor.ui.rendernode.model import RN_COL_INIT_WIDTH, RN_COL_DATA
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

    selectedRendernodesChanged = pyqtSignal(list)

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
        self.setHorizontalScrollMode(TableView.ScrollPerPixel)
        self.setVerticalScrollMode(TableView.ScrollPerPixel)
        self.setItemDelegateForColumn(RN_COL_DATA.index("ramUsage"), ProgressBarDelegate(self))
        self.setItemDelegateForColumn(RN_COL_DATA.index("systemSwapPercentage"), ProgressBarDelegate(self))
        self.setItemDelegateForColumn(RN_COL_DATA.index("excluded"), CheckBoxDelegate(self))
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.onContextMenu)

    def selectionChanged(self, selected, deselected):
        '''
        Slot called when the render nodes view table selection changes,
        notifying dependent widgets.
        :param selected: selected items
        :type selected: QItemSelection
        :param deselected: deselected items
        :type deselected: QItemSelection
        '''
        super(RenderNodeTableView, self).selectionChanged(selected, deselected)
        rns = list(set(idx.data(Qt.UserRole) for idx in selected.indexes()))
        self.selectedRendernodesChanged.emit(rns)

    def onContextMenu(self, pos):
        menu = QMenu(self)
        menu.addActions(self.actions())
        menu.exec_(QCursor.pos())
