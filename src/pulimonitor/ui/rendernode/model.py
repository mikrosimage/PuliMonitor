
from PyQt4.QtCore import QAbstractTableModel, Qt, QModelIndex, QDateTime
from PyQt4.QtGui import QColor, QSortFilterProxyModel, QStyle, qApp

from octopus.core.enums.rendernode import RN_STATUS_NAMES
from pulimonitor.network.requesthandler import RequestHandler


RN_COL_NAMES = ("Image", "ID", "Name", "Host", "Port", "Status", "Commands",
                "Pools", "Cores", "Cores Used", "Free Cores",
                "RAM", "Free RAM", "RAM Usage", "Swap Percentage",
                "Registred At", "Created At", "Last Time Alive", "Puli Version",
                "Speed", "Performance", "Excluded", "Characteristics")


RN_COL_DATA = ("image", "id", "name", "host", "port", "status", "commands",
               "pools", "coresNumber", "usedCoresNumber", "freeCoresNumber",
               "ramSize", "systemFreeRam", "ramUsage", "systemSwapPercentage",
               "registerDate", "createDate", "lastAliveTime", "puliversion",
               "speed", "performance", "excluded", "caracteristics")


RN_COL_INIT_WIDTH = (25, 25, 100, 100, 75)

RN_NUM_COLUMNS = len(RN_COL_DATA)

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
        self.requestHandler = RequestHandler()
        self.requestHandler.renderNodesUpdated.connect(self.onDataUpdate)
        self.rendernodes = []

    def onDataUpdate(self, updatedRendernodes):
        self.layoutAboutToBeChanged.emit()
        newRenderNodeIds = dict([(rn.id, (row, rn)) for row, rn in enumerate(updatedRendernodes)])
        for oldIndex in self.persistentIndexList():
            oldRendernode = oldIndex.data(Qt.UserRole)
            try:
                newRow, newRenderNode = newRenderNodeIds[oldRendernode.id]
                self.changePersistentIndex(oldIndex, self.createIndex(newRow, oldIndex.column(), newRenderNode))
            except KeyError:
                self.changePersistentIndex(oldIndex, QModelIndex())
        self.rendernodes = updatedRendernodes
        self.layoutChanged.emit()

    def rowCount(self, parent):
        return len(self.rendernodes)

    def columnCount(self, parent):
        return RN_NUM_COLUMNS

    def data(self, index, role):
        row = index.row()
        columnIndex = index.column()
        columnDataName = RN_COL_DATA[columnIndex]
        rendernode = self.rendernodes[row]
        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        if role == Qt.DisplayRole:
            if role == Qt.DisplayRole:
                if columnDataName == "status":
                    return RN_STATUS_NAMES[rendernode.status]
                if columnDataName == "ramSize":
                    return "{0} MB".format(rendernode.ramSize)
                if columnDataName == "systemFreeRam":
                    return "{0} MB".format(rendernode.systemFreeRam)
                elif columnDataName == "ramUsage":
                    total = float(rendernode.systemFreeRam)
                    return max(min(100.0, (rendernode.ramSize - total) / total * 100.0), 0.0)
                elif columnDataName == "registerDate":
                    return QDateTime.fromTime_t(int(rendernode.registerDate))
                elif columnDataName == "createDate":
                    return QDateTime.fromTime_t(int(rendernode.createDate))
                elif columnDataName == "lastAliveTime":
                    return QDateTime.fromTime_t(int(rendernode.lastAliveTime))
                else:
                    return getattr(rendernode, columnDataName, None)
        if role == Qt.BackgroundRole:
            if columnDataName == "status":
                return RN_STATUS_COLORS[rendernode.status]
        if role == Qt.UserRole:
            return rendernode
        if role == Qt.DecorationRole:
            if columnDataName == "image":
                return qApp.style().standardIcon(QStyle.SP_ComputerIcon)
        return None

    def flags(self, index):
        # We cannot do this to show the computer icon disabled due to a Qt 4.x
        # bug, which then makes the first column of the selected row
        # unselected upon changeing persisten indexes/data updating
        # columnName = RN_COL_DATA[index.column()]
        # if columnName == "image":
        #    rendernode = self.rendernodes[index.row()]
        #    if rendernode.status == RN_UNKNOWN:
        #        return Qt.ItemIsSelectable
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return RN_COL_NAMES[section]
        else:
            return None
