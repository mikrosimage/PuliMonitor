from PyQt4.QtCore import QAbstractItemModel, Qt, QModelIndex

from treeitem import TreeItem


class TreeModel(QAbstractItemModel):

    def __init__(self, parent=None):
        super(TreeModel, self).__init__(parent)
        self.columns = []
        self.__columnCount = 0
        self.rootItem = TreeItem(None, None)

    def setColumns(self, columns):
        self.columns = columns
        self.__columnCount = len(columns)

    def columnCount(self, parent):
        return self.__columnCount

    def data(self, index, role):
        if not index.isValid():
            return None
        item = index.internalPointer()
        return item.data(index, role)

    def flags(self, index):
        if index.isValid():
            item = index.internalPointer()
            return item.flags(index)
        return Qt.NoItemFlags

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.columns[section]
        return None

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()
        childItem = index.internalPointer()
        parentItem = childItem.parent
        if not parentItem or parentItem == self.rootItem:
            return QModelIndex()
        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()
        return parentItem.childCount()
