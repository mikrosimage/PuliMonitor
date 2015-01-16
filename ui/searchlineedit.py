from PyQt4.QtCore import pyqtSignal, Qt
from PyQt4.QtGui import QLineEdit, QToolButton, QIcon, QStyle, QApplication

from resources import icons  # @UnusedImport


class SearchLineEdit(QLineEdit):
    '''
    A search widget with icon and a "clear" button
    '''

    cleared = pyqtSignal()

    def __init__(self, parent=None):
        QLineEdit.__init__(self, parent)

        self.clearButton = QToolButton(self)
        self.clearButton.setIcon(QIcon(":/trolltech/styles/commonstyle/images/standardbutton-closetab-16.png"))
        self.clearButton.setCursor(Qt.ArrowCursor)
        self.clearButton.setStyleSheet("QToolButton { border: none;"
                                       "padding: 0px;"
                                       "padding-top:2px}")
        self.clearButton.hide()
        self.clearButton.clicked.connect(self.clear)
        self.clearButton.clicked.connect(self.cleared.emit)
        self.textChanged.connect(self.updateCloseButton)

        self.searchButton = QToolButton(self)
        self.searchButton.setIcon(QIcon(":/search.png"))
        self.searchButton.setStyleSheet("QToolButton { border: none; "
                                        "padding:0px;"
                                        "padding-top:2px;"
                                        "padding-left:5px}")

        frameWidth = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
        self.setStyleSheet("QLineEdit {padding-left: %spx;"
                           "padding-right: %spx; } " % (self.searchButton.sizeHint().width() + frameWidth + 1,
                                                        self.clearButton.sizeHint().width() + frameWidth + 1))
        msz = self.minimumSizeHint()
        self.setMinimumSize(max(msz.width(), self.searchButton.sizeHint().width() + self.clearButton.sizeHint().width() + frameWidth * 2 + 2),
                            max(msz.height(), self.clearButton.sizeHint().height() + frameWidth * 2 + 2))

    def resizeEvent(self, event):
        '''
        Reimplemented to move the pixmaps once the geometry changes
        :type event: QResizeEvent
        '''
        sz = self.clearButton.sizeHint()
        frameWidth = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
        self.clearButton.move(self.rect().right() - frameWidth - sz.width(),
                              (self.rect().bottom() + 1 - sz.height()) / 2)
        self.searchButton.move(self.rect().left() + 1,
                               (self.rect().bottom() + 1 - sz.height()) / 2)

    def updateCloseButton(self, text):
        '''
        Shows/hides the close button according to the inputs text state
        :param text: user text
        :type text: str
        '''
        if text:
            self.clearButton.setVisible(True)
        else:
            self.clearButton.setVisible(False)

    def setModel(self, model):
        self.__model = model
        self.textEdited.connect(model.setFilterFixedString)


def main():
    import sys
    app = QApplication([])
    w = SearchLineEdit()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
