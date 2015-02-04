from PyQt4.QtCore import Qt
from PyQt4.QtGui import QStyledItemDelegate, QStyle, QApplication, \
    QStyleOptionButton


class CheckBoxDelegate(QStyledItemDelegate):
    '''
    A  delegate able to display the cell value as a checkbox.
    '''

    def __init__(self, parent=None):
        super(CheckBoxDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        '''
        Reimplemented from QStyledItemDelegate.

        :type painter: QPainter
        :type option: QStyleOption
        :type index: QModelIndex
        '''

        checked = index.data()
        buttonOption = QStyleOptionButton()
        buttonOption.rect = option.rect
        buttonOption.textAlignment = Qt.AlignCenter
        buttonOption.state = QStyle.State_On if checked else QStyle.State_Off

        QApplication.style().drawControl(QStyle.CE_CheckBox, buttonOption, painter)
