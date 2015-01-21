
from PyQt4.QtCore import QAbstractTableModel, Qt, QModelIndex
from PyQt4.QtGui import QColor, QSortFilterProxyModel, QStyle, qApp

from octopus.core.enums.rendernode import RN_STATUS_NAMES


# TODO: add these columns
# RENDERNODE_COLUMNS = {"Characteristics": u'caracteristics',
#                       "Registered": u'isRegistered',
#                       "Excluded": u'excluded',
#                       "Speed": u'speed',
#                       "Puli Version": u'puliversion',
#                       "Creation Date": u'createDate',
#                       "Port": u'port',
#                       "Performance": u'performance',
#                       "Last Time Available": u'lastAliveTime',
#                       "Swap Percentage": u'systemSwapPercentage',
#                       "Registration Date": u'registerDate'}

RN_COL_NAMES = ("Image", "ID", "Name", "Host", "Status", "Commands", "Pools",
                "Cores", "Cores Used", "Free Cores",
                "RAM", "Free RAM", "RAM Usage")
RN_COL_DATA = ("image", "id", "name", "host", "status", "commands", "pools",
               "coresNumber", "usedCoresNumber", "freeCoresNumber",
               "ramSize", "systemFreeRam", "ramUsage")
RN_COL_INIT_WIDTH = (25, 25, 100, 100, 75)

RN_NUM_COLUMNS = len(RN_COL_NAMES)

RN_STATUS_COLORS = (QColor(Qt.darkGray),
                    QColor(Qt.lightGray),
                    QColor(Qt.magenta),
                    QColor(Qt.transparent),
                    QColor(Qt.cyan),
                    QColor(Qt.blue),
                    QColor(Qt.darkBlue))


class RenderNodeTableProxyModel(QSortFilterProxyModel):

    def __init__(self, sourceModel, parent=None):
        super(RenderNodeTableProxyModel, self).__init__(parent)
        self.setSourceModel(sourceModel)
        self.setFilterKeyColumn(-1)
        self.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.setDynamicSortFilter(True)


class RenderNodeTableModel(QAbstractTableModel):

    def __init__(self, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.rows = []

    def onDataUpdate(self, requestData):
        self.layoutAboutToBeChanged.emit()
        pIndexes = dict([(index.data(Qt.UserRole)["id"], index) for index in self.persistentIndexList()])
        self.rows = requestData
        for rowNum, row in enumerate(self.rows):
            oldIndex = pIndexes.pop(row["id"], None)
            if oldIndex:
                self.changePersistentIndex(oldIndex, self.createIndex(rowNum, oldIndex.column(), row))
        for _rnId, oldIndex in pIndexes:
            self.changePersistentIndex(oldIndex, QModelIndex())
        self.layoutChanged.emit()

    def rowCount(self, parent):
        return len(self.rows)

    def columnCount(self, parent):
        return RN_NUM_COLUMNS

    def data(self, index, role):
        row = index.row()
        columnIndex = index.column()
        columnName = RN_COL_NAMES[columnIndex]
        rowData = self.rows[row]
        data = rowData.get(RN_COL_DATA[columnIndex])
        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        if role == Qt.DisplayRole:
            if role == Qt.DisplayRole:
                if columnName == "Status":
                    return RN_STATUS_NAMES[data]
                elif columnName == "RAM Usage":
                    return rowData["systemFreeRam"] / float(rowData["ramSize"]) * 100.0
                else:
                    return data
        if role == Qt.BackgroundRole:
            if columnName == "Status":
                return RN_STATUS_COLORS[data]
        if role == Qt.UserRole:
            return rowData
        if role == Qt.DecorationRole:
            if columnName == "Image":
                # TODO: user deactivated style once the host status is down
                return qApp.style().standardIcon(QStyle.SP_ComputerIcon)

        return None

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return RN_COL_NAMES[section]
        else:
            return None
