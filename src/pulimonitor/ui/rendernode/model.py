
from PyQt4.QtCore import QAbstractTableModel, Qt, QModelIndex
from PyQt4.QtGui import QColor, QSortFilterProxyModel, QStyle, qApp

from octopus.core.enums.rendernode import RN_STATUS_NAMES, RN_UNKNOWN
from pulimonitor.network.requesthandler import RequestHandler


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

    def onDataUpdate(self, rendernodes):
        self.layoutAboutToBeChanged.emit()
        pIndexes = dict([(index.data(Qt.UserRole).id, index) for index in self.persistentIndexList()])
        self.rendernodes = rendernodes
        for rowNum, rendernode in enumerate(self.rendernodes):
            oldIndex = pIndexes.pop(rendernode.id, None)
            if oldIndex:
                self.changePersistentIndex(oldIndex,
                                           self.createIndex(rowNum,
                                                            oldIndex.column(),
                                                            rendernode))
        for _rnId, oldIndex in pIndexes.iteritems():
            self.changePersistentIndex(oldIndex, QModelIndex())
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
        columnName = RN_COL_DATA[index.column()]
        if columnName == "image":
            rendernode = self.rendernodes[index.row()]
            if rendernode.status == RN_UNKNOWN:
                return Qt.ItemIsSelectable
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return RN_COL_NAMES[section]
        else:
            return None
