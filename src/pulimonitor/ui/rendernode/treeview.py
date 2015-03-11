from PyQt4.QtCore import Qt, pyqtSignal, QModelIndex
from PyQt4.QtGui import QAbstractItemView, QMenu, QCursor, QStyledItemDelegate

from pulimonitor.ui.checkboxdelegate import CheckBoxDelegate
from pulimonitor.ui.headerview import HeaderView
from pulimonitor.ui.progressbardelegate import ProgressBarDelegate
from pulimonitor.ui.rendernode.treemodel import RN_COL_DATA, RenderNodeTreeItem, \
    RN_COL_INIT_HIDDEN, RN_COL_INIT_WIDTH
from pulimonitor.ui.treeview import TreeView
from pulimonitor.util import config


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
        return RN_COL_INIT_HIDDEN


class RenderNodeProgressBarDelegate(ProgressBarDelegate):

    def __init__(self, parent=None):
        super(RenderNodeProgressBarDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        if isinstance(index.data(Qt.UserRole), RenderNodeTreeItem):
            return super(RenderNodeProgressBarDelegate, self).paint(painter, option, index)
        QStyledItemDelegate.paint(self, painter, option, index)


class RenderNodeCheckBoxDelegate(CheckBoxDelegate):

    def __init__(self, parent=None):
        super(RenderNodeCheckBoxDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        if isinstance(index.data(Qt.UserRole), RenderNodeTreeItem):
            return super(RenderNodeCheckBoxDelegate, self).paint(painter, option, index)
        QStyledItemDelegate.paint(self, painter, option, index)


class RenderNodeTreeView(TreeView):
    '''
    Subclass providing a context menu and custom settings for the render nodes
    table view.
    '''

    selectedRendernodesChanged = pyqtSignal(list)

    def __init__(self, parent=None):
        super(RenderNodeTreeView, self).__init__(parent)
        self.setSortingEnabled(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setHeader(RenderNodeHeaderView(Qt.Horizontal))
        self.header().setColumnsHidable(True)
        self.header().setMovable(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.onContextMenu)
        self.setUniformRowHeights(True)
        self.setAllColumnsShowFocus(True)
        self.setItemDelegateForColumn(RN_COL_DATA.index("ramUsage"), RenderNodeProgressBarDelegate(self))
        self.setItemDelegateForColumn(RN_COL_DATA.index("systemSwapPercentage"), RenderNodeProgressBarDelegate(self))
        self.setItemDelegateForColumn(RN_COL_DATA.index("excluded"), RenderNodeCheckBoxDelegate(self))

    def onLayoutChanged(self):
        for row in range(self.model().rowCount()):
            self.setFirstColumnSpanned(row, QModelIndex(), True)

    def selectionChanged(self, selected, deselected):
        '''
        Slot called when the render nodes view table selection changes,
        notifying dependent widgets.
        :param selected: selected items
        :type selected: QItemSelection
        :param deselected: deselected items
        :type deselected: QItemSelection
        '''
        super(RenderNodeTreeView, self).selectionChanged(selected, deselected)
        rns = list(set(idx.data(Qt.UserRole) for idx in selected.indexes()))
        self.selectedRendernodesChanged.emit(rns)

    def onContextMenu(self, pos):
        menu = QMenu(self)
        menu.addActions(self.actions())
        menu.exec_(QCursor.pos())

    def setModel(self, *args, **kwargs):
        TreeView.setModel(self, *args, **kwargs)
        if config.get().getboolean("RenderNodeView", "group_by_pool"):
            self.model().layoutChanged.connect(self.onLayoutChanged)
