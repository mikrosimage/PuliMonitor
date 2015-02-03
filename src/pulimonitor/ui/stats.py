'''
Created on Jan 27, 2015

@author: Sebastian Elsner
@organization: rise|fx GmbH
'''
from PyQt4.QtGui import QWidget, QLabel, QHBoxLayout, QApplication

from pulimonitor.network.requesthandler import RequestHandler
from pulimonitor.ui.misc import VLine


class StatsWidget(QWidget):

    def __init__(self, parent=None):
        super(StatsWidget, self).__init__(parent)
        self.mainLayout = QHBoxLayout(self)
        self.mainLayout.setMargin(2)
        self.mainLayout.addStretch()
        self.setLayout(self.mainLayout)
        self.statLabels = {}
        self.__firstVLine = True
        self.rh = RequestHandler()
        self.rh.renderNodesStatsChanged

    def onStatsChanged(self, stats):
        for statName, statValue in stats:
            label = self.statLabels.get(statName)
            if not label:
                label = QLabel(self)
                if self.__firstVLine:
                    self.__firstVLine = False
                else:
                    self.mainLayout.addWidget(VLine(self))
                self.mainLayout.addWidget(label)
                self.statLabels[statName] = label
            label.setText("%s: %s" % (statName, statValue))


if __name__ == '__main__':
    app = QApplication([])
    w = StatsWidget()
    w.onStatsChanged((("total", 2), ("offline", 3)))
    w.show()
    app.exec_()
