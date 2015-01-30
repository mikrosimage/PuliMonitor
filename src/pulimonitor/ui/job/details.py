from PyQt4.QtGui import QFormLayout, QApplication, QLineEdit, QGroupBox

from pulimonitor.ui.job.model import JOB_COL_DATA, JOB_COL_NAMES


class JobDetails(QGroupBox):

    def __init__(self, parent=None):
        super(JobDetails, self).__init__(parent)
        layout = QFormLayout(self)
        self.dataWidgets = {}
        for name, dataName in zip(JOB_COL_NAMES, JOB_COL_DATA):
            lineedit = QLineEdit(self)
            self.dataWidgets[dataName] = lineedit
            layout.addRow(name, lineedit)

    def refresh(self, row):
        for key, value in row.iteritems():
            if key in self.dataWidgets:
                self.dataWidgets[key].setText(str(value))


def main():
    import sys
    app = QApplication([])
    w = JobDetails()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
