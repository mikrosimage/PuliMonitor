from PyQt4.QtGui import QFormLayout, QApplication, QLineEdit, QGroupBox

from pulimonitor.ui.rendernode.model import RN_COL_NAMES, RN_COL_DATA

# TODO: make scrollable


class RenderNodeDetails(QGroupBox):

    def __init__(self, parent=None):
        super(RenderNodeDetails, self).__init__(parent)
        layout = QFormLayout(self)
        self.dataWidgets = {}
        for name, dataName in zip(RN_COL_NAMES, RN_COL_DATA):
            lineedit = QLineEdit(self)
            self.dataWidgets[dataName] = lineedit
            layout.addRow(name, lineedit)

    def refresh(self, rendernodes):
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
