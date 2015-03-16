'''
Created on Jan 27, 2015

@author: Sebastian Elsner
@organization: rise|fx GmbH
'''
from pulimonitor.network import requesthandler
from pulimonitor.ui.stats import StatsWidget


class RenderNodeStatsWidget(StatsWidget):

    def __init__(self, parent=None):
        super(RenderNodeStatsWidget, self).__init__(parent)
        rh = requesthandler.get()
        rh.renderNodesStatsChanged.connect(self.onStatsChanged)
