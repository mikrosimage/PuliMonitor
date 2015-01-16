from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QTableView


class TableView(QTableView):
    '''
    Extended QTableView allowing to deselect rows by clicking on empty space
    and supporting the custom HeaderView.
    '''

    rowSelectionChanged = pyqtSignal(object)

    def __init__(self, parent=None):
        QTableView.__init__(self, parent)
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
            return QTableView.mousePressEvent(self, event)
        elif self.__isClearable:
            self.selectionModel().clear()

    def setModel(self, *args, **kwargs):
        '''
        Reimplemented to apply section settings AFTER the model was set. This
        is the only way to implement this behaviour since the sections are
        reset when the model is applied the first time.
        '''
        QTableView.setModel(self, *args, **kwargs)
        self.horizontalHeader().applySectionSettings()
