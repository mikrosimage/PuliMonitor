from PyQt4.QtGui import QFormLayout, QApplication, QLineEdit, QScrollArea, QDockWidget, \
    QWidget

from pulimonitor.ui.rendernode.model import RN_COL_NAMES, RN_COL_DATA
from uuid import uuid4


class RenderNodeDetails(QDockWidget):

    def __init__(self, parent=None):
        super(RenderNodeDetails, self).__init__("rendernode details", parent)
        self.setObjectName("rendernodedetails-dock-{0}".format(uuid4().hex))
        scrollArea = QScrollArea(self)
        scrollArea.setWidgetResizable(True)
        scrollAreaContentsWidget = QWidget()
        formLayout = QFormLayout(scrollAreaContentsWidget)
        self.dataWidgets = {}
        for name, dataName in zip(RN_COL_NAMES, RN_COL_DATA):
            lineedit = QLineEdit(scrollAreaContentsWidget)
            self.dataWidgets[dataName] = lineedit
            formLayout.addRow(name, lineedit)
        scrollArea.setWidget(scrollAreaContentsWidget)
        self.setWidget(scrollArea)

    def onRendernodeChanged(self, rendernodes):
        for rendernode in rendernodes:
            for dataName in RN_COL_DATA:
                if dataName in self.dataWidgets:
                    self.dataWidgets[dataName].setText(str(getattr(rendernode, dataName, "")))
            break


def main():
    import sys
    app = QApplication([])
    w = RenderNodeDetails()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
