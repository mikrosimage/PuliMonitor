'''
Created on Feb 19, 2015

@author: sebels
'''

import time

from PyQt4.QtCore import Qt, QModelIndex, QDateTime, QSize
from PyQt4.QtGui import QColor, QSortFilterProxyModel, qApp, QStyle
from cached_property import cached_property

from octopus.core.enums.rendernode import RN_STATUS_NAMES
from pulimonitor.network.requesthandler import RequestHandler
from pulimonitor.ui.misc import dictToHtmlTable
from pulimonitor.ui.treeitem import TreeItem
from pulimonitor.ui.treemodel import TreeModel
from pulimonitor.util import config


RN_COL_NAMES = ("", "ID", "Name", "Host", "Port", "Status", "Commands",
                "Pools", "Cores",
                "RAM", "Free RAM", "RAM Usage", "Swap Percentage",
                "Registred At", "Created At", "Last Time Alive", "Puli Version",
                "Speed", "Performance", "Excluded", "Characteristics")


RN_COL_DATA = ("", "id", "name", "host", "port", "status", "commands",
               "pools", "coresNumber",
               "ramSize", "systemFreeRam", "ramUsage", "systemSwapPercentage",
               "registerDate", "createDate", "lastAliveTime", "puliversion",
               "speed", "performance", "excluded", "caracteristics")

DEFAULT_WIDTH = 100
RN_COL_INIT_WIDTH = (60, 25, DEFAULT_WIDTH, 125, 75, DEFAULT_WIDTH, DEFAULT_WIDTH,
                     DEFAULT_WIDTH, DEFAULT_WIDTH,
                     DEFAULT_WIDTH, DEFAULT_WIDTH, DEFAULT_WIDTH, DEFAULT_WIDTH,
                     DEFAULT_WIDTH, DEFAULT_WIDTH, DEFAULT_WIDTH, DEFAULT_WIDTH,
                     DEFAULT_WIDTH, DEFAULT_WIDTH, DEFAULT_WIDTH, DEFAULT_WIDTH)

RN_COL_INIT_HIDDEN = (0, 1, 1, 0, 1, 0, 0,
                      1, 0,
                      1, 1, 0, 0,
                      1, 1, 1, 1,
                      1, 1, 1, 1)

RN_NUM_COLUMNS = len(RN_COL_DATA)

RN_STATUS_COLORS = (QColor(Qt.darkGray),
                    QColor(Qt.lightGray),
                    QColor(Qt.magenta),
                    QColor(Qt.transparent),
                    QColor(Qt.cyan),
                    QColor(Qt.blue),
                    QColor(Qt.darkBlue))


class PoolTreeItem(TreeItem):

    def __init__(self, data, parent):
        super(PoolTreeItem, self).__init__(data, parent)
        self.id = self._data

    def data(self, index, role):
        columnIndex = index.column()
        columnDataName = RN_COL_DATA[columnIndex]
        if role == Qt.DisplayRole:
            if columnDataName == "":
                return self._data
        if role == Qt.UserRole:
            return self
        if role == Qt.DecorationRole:
            if columnDataName == "":
                return qApp.style().standardIcon(QStyle.SP_DriveNetIcon)
        if role == Qt.SizeHintRole:
            return QSize(100, 30)
        else:
            return None


class RenderNodeTreeItem(TreeItem):

    def __init__(self, data, pool, parent):
        super(RenderNodeTreeItem, self).__init__(data, parent)
        self.id = pool + "/" + self._data.name

    @cached_property
    def ramUsageDisplay(self):
        total = float(self._data.systemFreeRam)
        return max(min(100.0, (self._data.ramSize - total) / total * 100.0), 0.0)

    @cached_property
    def registerDate(self):
        return QDateTime.fromTime_t(int(self._data.registerDate))

    @cached_property
    def createDate(self):
        return QDateTime.fromTime_t(int(self._data.createDate))

    @cached_property
    def lastAliveTime(self):
        return QDateTime.fromTime_t(int(self._data.lastAliveTime))

    @cached_property
    def systemFreeRam(self):
        return "{0} MB".format(self._data.systemFreeRam)

    @cached_property
    def ramSize(self):
        return "{0} MB".format(self._data.ramSize)

    @cached_property
    def statusName(self):
        return RN_STATUS_NAMES[self._data.status]

    @cached_property
    def statusColor(self):
        return RN_STATUS_COLORS[self._data.status]

    def data(self, index, role):
        columnIndex = index.column()
        columnDataName = RN_COL_DATA[columnIndex]
        if role == Qt.DisplayRole:
            if columnDataName == "status":
                return self.statusName
            if columnDataName == "ramSize":
                return self.ramSize
            if columnDataName == "systemFreeRam":
                return self.systemFreeRam
            elif columnDataName == "ramUsage":
                return self.ramUsageDisplay
            elif columnDataName == "registerDate":
                return self.registerDate
            elif columnDataName == "createDate":
                return self.createDate
            elif columnDataName == "lastAliveTime":
                return self.lastAliveTime
            elif columnDataName == "caracteristics":
                return str(self._data.caracteristics)
            else:
                return getattr(self._data, columnDataName, None)
        if role == Qt.ToolTipRole:
            if columnDataName == "caracteristics":
                return dictToHtmlTable(self._data.caracteristics)
        if role == Qt.SizeHintRole:
            return QSize(RN_COL_INIT_WIDTH[columnIndex], 30)
        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        if role == Qt.BackgroundRole:
            if columnDataName == "status":
                return self.statusColor
        if role == Qt.UserRole:
            return self
        if role == Qt.DecorationRole:
            if columnDataName == "":
                return qApp.style().standardIcon(QStyle.SP_ComputerIcon)
        else:
            return None


class RenderNodeProxyModel(QSortFilterProxyModel):

    def __init__(self, sourceModel, parent=None):
        super(RenderNodeProxyModel, self).__init__(parent)
        self.setSourceModel(sourceModel)
        self.setFilterKeyColumn(-1)
        self.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.setDynamicSortFilter(True)


class RenderNodeModel(TreeModel):

    def __init__(self, parent=None):
        super(RenderNodeModel, self).__init__(parent)
        self.setColumns(RN_COL_NAMES)
        self.requestHandler = RequestHandler()
        self.requestHandler.renderNodesUpdated.connect(self.onDataUpdate)

    def buildTree(self, updatedRendernodes, treeItemsById):
        for rendernode in updatedRendernodes:
            for pool in rendernode.pools or ["default"]:
                pti = treeItemsById.get(pool)
                if not pti:
                    pti = PoolTreeItem(pool, self.rootItem)
                    treeItemsById[pool] = pti
                rnti = RenderNodeTreeItem(rendernode, pool, pti)
                treeItemsById[rnti.id] = rnti

    def buildTable(self, updatedRendernodes, treeItemsById):
        for rendernode in updatedRendernodes:
            rnti = RenderNodeTreeItem(rendernode, "default", self.rootItem)
            treeItemsById[rnti.id] = rnti

    def onDataUpdate(self, updatedRendernodes):
        tree = config.get().getboolean("RenderNodeView", "group_by_pool")
        t1 = time.time()
        self.layoutAboutToBeChanged.emit()
        _oldRoot = self.rootItem  # rescue old root from garbage collector
        self.rootItem = TreeItem(None, None)
        treeItemsById = {}
        if tree:
            self.buildTree(updatedRendernodes, treeItemsById)
        else:
            self.buildTable(updatedRendernodes, treeItemsById)

        for oldIndex in self.persistentIndexList():
            oldTreeItem = oldIndex.data(Qt.UserRole)
            newTreeItem = treeItemsById.get(oldTreeItem.id)
            if newTreeItem:
                self.changePersistentIndex(oldIndex, self.createIndex(newTreeItem.row(), oldIndex.column(), newTreeItem))
            else:
                self.changePersistentIndex(oldIndex, QModelIndex())

        self.layoutChanged.emit()
        print time.time() - t1
