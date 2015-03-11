from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QTreeView


class TreeView(QTreeView):
    '''
    Extended QTreeView allowing to deselect rows by clicking on empty space
    and supporting the custom HeaderView.
    '''

    rowSelectionChanged = pyqtSignal(object)

    def __init__(self, parent=None):
        QTreeView.__init__(self, parent)
        self.__isClearable = False

    def setSelectionClearable(self, value):
        '''
        If the clearable selection is activated a user can click on an empty space
        in the view to deselect the current selection
        :type value: boolean
        '''
        self.__isClearable = value

    def mousePressEvent(self, event):
        '''
        Reimplement to make view clearable
        '''
        index = self.indexAt(event.pos())
        if index.isValid():
            return QTreeView.mousePressEvent(self, event)
        elif self.__isClearable:
            self.selectionModel().clear()

    def setModel(self, *args, **kwargs):
        '''
        Reimplemented to apply section settings AFTER the model was set. This
        is the only way to implement this behavior since the sections are
        reset when the model is applied the first time.
        The same applies to connecting to the selectionChanged signal, which is
        used to notify selection sensitive Actions to enable or
        disable themselves.
        '''
        QTreeView.setModel(self, *args, **kwargs)
        self.header().applySectionSettings()

    def selectionChanged(self, selected, deselected):
        '''
        Reimplemented slot called when the views selection changes. Iterates
        over all Actions registered with this view to update their 'enabled'
        status depending on the current selection.
        :param selected: selected items
        :type selected: QItemSelection
        :param deselected: deselected items
        :type deselected: QItemSelection
        '''
        super(TreeView, self).selectionChanged(selected, deselected)
        hasSelection = self.selectionModel().hasSelection()
        for action in self.actions():
            action.setEnabledOnSelectionChange(hasSelection)
