from PyQt4.QtCore import Qt
from PyQt4.QtGui import QHeaderView, QMenu, QAction, QCursor


class HeaderView(QHeaderView):
    '''
    Extended QHeaderView class allowing columns to be hidden.
    '''

    def __init__(self, orientation, parent=None):
        QHeaderView.__init__(self, orientation, parent)
        self.originalContextMenuPolicy = self.contextMenuPolicy()

    def setColumnsHidable(self, value):
        '''
        Set columns to be hideable.
        :param value: turn this feature on or off by passing True/False
        :type value: boolean
        '''
        if value:
            self.setContextMenuPolicy(Qt.CustomContextMenu)
            self.customContextMenuRequested.connect(self.showHeaderContextMenu)
        else:
            self.setContextMenuPolicy(self.originalContextMenuPolicy)
            self.customContextMenuRequested.disconnect(self.showHeaderContextMenu)

    def showHeaderContextMenu(self, pos):
        '''
        The slot called once the header was right clicked.
        :param pos: position of the click
        :type pos: QPoint
        '''
        menu = QMenu(self)
        for section in range(self.count()):
            columnName = self.model().sourceModel().headerData(section, Qt.Horizontal, Qt.DisplayRole)
            isHidden = self.isSectionHidden(section)
            action = QAction(columnName, menu)
            action.setCheckable(True)
            action.setChecked(not isHidden)
            action.setData(section)
            action.toggled.connect(self.sectionVisibilityToggled)
            menu.addAction(action)
        menu.exec_(QCursor.pos())

    def sectionVisibilityToggled(self, checked):
        '''
        Slot called once a section has been ticked/unticked in the header
        :param checked: boolean value indicating the visibility
        :type checked: boolean
        '''
        action = self.sender()
        logicalIndex = action.data()
        self.setSectionHidden(logicalIndex, not checked)

    def applySectionSettings(self):
        '''
        Applies all section settings: initial section size, intitial resize mode,
        initial section visibility
        '''

        for section, value in enumerate(self.sectionSizes()):
            self.resizeSection(section, value)
        for section, value in enumerate(self.sectionResizeModes()):
            self.setResizeMode(section, value)
        for section, value in enumerate(self.sectionHiddenStatus()):
            self.setSectionHidden(section, value)

    def sectionSizes(self):
        '''
        Reimplement this method returning a list of integer section withs
        '''
        return []

    def sectionResizeModes(self):
        '''
        Reimplement this method returning a list of Qt.ResizeModes
        '''

        return []

    def sectionHiddenStatus(self):
        '''
        Reimplement this method returning a list of boolean values indicating
        each section visibility.
        '''
        return []
