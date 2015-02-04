from PyQt4.QtCore import Qt
from PyQt4.QtGui import QStyledItemDelegate, QStyle, QApplication, QStyleOptionProgressBarV2


class ProgressBarDelegate(QStyledItemDelegate):
    '''
    A  delegate able to display the cell value as a progress bar.
    '''

    def __init__(self, parent=None):
        super(ProgressBarDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        '''
        Reimplemented from QStyledItemDelegate.

        :type painter: QPainter
        :type option: QStyleOption
        :type index: QModelIndex
        '''

        progress = index.data()

        progressBarStyleOption = QStyleOptionProgressBarV2()
        progressBarStyleOption.rect = option.rect
        progressBarStyleOption.minimum = 0
        progressBarStyleOption.maximum = 100
        progressBarStyleOption.textAlignment = Qt.AlignCenter
        progressBarStyleOption.progress = progress
        progressBarStyleOption.text = "{0:.2}%".format(float(progress))
        progressBarStyleOption.textVisible = True

        QApplication.style().drawControl(QStyle.CE_ProgressBar, progressBarStyleOption, painter)
