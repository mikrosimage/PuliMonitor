
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QColor, QSortFilterProxyModel

from ui.treemodel import TreeModel


JOB_COL_NAMES = ("Image", "ID", "Name")
JOB_COL_DATA = ("image", "id", "name")
JOB_COL_INIT_WIDTH = (25, 25, 100)

JOB_NUM_COLUMNS = len(JOB_COL_NAMES)

JOB_STATUS_COLORS = (QColor(Qt.darkGray),
                     QColor(Qt.lightGray),
                     QColor(Qt.magenta),
                     QColor(Qt.transparent),
                     QColor(Qt.cyan),
                     QColor(Qt.blue),
                     QColor(Qt.darkBlue))


class JobTreeProxyModel(QSortFilterProxyModel):

    def __init__(self, sourceModel, parent=None):
        super(JobTreeProxyModel, self).__init__(parent)
        self.setSourceModel(sourceModel)
        self.setFilterKeyColumn(-1)
        self.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.setDynamicSortFilter(True)


class JobTreeModel(TreeModel):

    def __init__(self, parent=None):
        TreeModel.__init__(self, parent)
        self.setColumns(JOB_COL_NAMES)

    def onDataUpdate(self, requestData):
        print requestData
