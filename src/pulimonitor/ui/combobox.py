from PyQt4.QtGui import QComboBox
from PyQt4.QtCore import pyqtSignal


class ComboBox(QComboBox):

    currentItemChanged = pyqtSignal(object)
    currentTextChanged = pyqtSignal(object)

    def __init__(self, parent=None):
        super(ComboBox, self).__init__(parent)
        self.currentIndexChanged.connect(self._currentItemChanged)
        self.currentIndexChanged.connect(self._currentTextChanged)

    def _currentItemChanged(self, index):
        self.currentItemChanged.emit(self.itemData(index))

    def _currentTextChanged(self, index):
        self.currentTextChanged.emit(self.currentText())

    def currentItemData(self):
        return self.itemData(self.currentIndex())
