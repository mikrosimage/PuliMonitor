
from PyQt4.QtCore import QAbstractTableModel, Qt, QModelIndex
from PyQt4.QtGui import QColor, QSortFilterProxyModel, QStyle, qApp

from pulimonitor.network.requesthandler import RequestHandler
from octopus.core.enums.rendernode import RN_STATUS_NAMES


COL_NAMES = ("Image", "ID", "Name", "Pool Shares", "Rendernodes")
COL_DATA = ("image", "id", "name", "poolShares", "renderNodes")
COL_INIT_WIDTH = (25, 25, 100, 200, 200)

NUM_COLUMNS = len(COL_NAMES)

STATUS_COLORS = (QColor(Qt.darkGray),
                 QColor(Qt.lightGray),
                 QColor(Qt.magenta),
                 QColor(Qt.transparent),
                 QColor(Qt.cyan),
                 QColor(Qt.blue),
                 QColor(Qt.darkBlue))


class PoolTableProxyModel(QSortFilterProxyModel):

    def __init__(self, sourceModel, parent=None):
        super(PoolTableProxyModel, self).__init__(parent)
        self.setSourceModel(sourceModel)
        self.setFilterKeyColumn(-1)
        self.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.setDynamicSortFilter(True)


class PoolTableModel(QAbstractTableModel):

    def __init__(self, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.requestHandler = RequestHandler()
        self.requestHandler.poolsUpdated.connect(self.onDataUpdate)
        self.rows = []

    def onDataUpdate(self, requestData):
        self.layoutAboutToBeChanged.emit()
        pIndexes = dict([(index.data(Qt.UserRole)["id"], index) for index in self.persistentIndexList()])
        self.rows = requestData
        for rowNum, row in enumerate(self.rows):
            oldIndex = pIndexes.pop(row["id"], None)
            if oldIndex:
                self.changePersistentIndex(oldIndex, self.createIndex(rowNum, oldIndex.column(), row))
        for _rnId, oldIndex in pIndexes.iteritems():
            self.changePersistentIndex(oldIndex, QModelIndex())
        self.layoutChanged.emit()

    def rowCount(self, parent):
        return len(self.rows)

    def columnCount(self, parent):
        return NUM_COLUMNS

    def data(self, index, role):
        row = index.row()
        columnIndex = index.column()
        columnName = COL_NAMES[columnIndex]
        rowData = self.rows[row]
        data = rowData.get(COL_DATA[columnIndex])
        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        if role == Qt.DisplayRole:
            if role == Qt.DisplayRole:
                if columnName == "Status":
                    return RN_STATUS_NAMES[data]
                else:
                    return data
        if role == Qt.BackgroundRole:
            if columnName == "Status":
                return STATUS_COLORS[data]
        if role == Qt.UserRole:
            return rowData
        if role == Qt.DecorationRole:
            if columnName == "Image":
                return qApp.style().standardIcon(QStyle.SP_DriveNetIcon)

        return None

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return COL_NAMES[section]
        else:
            return None
