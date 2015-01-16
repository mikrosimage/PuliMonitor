from PyQt4.QtCore import Qt
from PyQt4.QtGui import QStyledItemDelegate, QStyleOptionProgressBar, qApp, QStyle


class ProgressBarDelegate(QStyledItemDelegate):
    '''
    A  delegate able to display the cell value as a progress bar. The cell value
    needs to be an integer.
    '''

    def paint(self, painter, option, index):
        '''
        Reimplemented from QStyledItemDelegate.

        :type painter: QPainter
        :type option: QStyleOption
        :type index: QModelIndex
        '''

        progressBarStyleOption = QStyleOptionProgressBar()
        progressBarStyleOption.rect = option.rect

        progress = index.data()

        progressBarStyleOption.minimum = 0
        progressBarStyleOption.maximum = 100
        progressBarStyleOption.textAlignment = Qt.AlignCenter
        progressBarStyleOption.progress = progress
        progressBarStyleOption.text = "{0:.2}%".format(progress)
        progressBarStyleOption.textVisible = True

        qApp.style().drawControl(QStyle.CE_ProgressBar, progressBarStyleOption, painter)
