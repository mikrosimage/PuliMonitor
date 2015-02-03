'''
Created on Jan 27, 2015

@author: Sebastian Elsner
@organization: rise|fx GmbH
'''
from pulimonitor.ui.stats import StatsWidget
from pulimonitor.network.requesthandler import RequestHandler


class RenderNodeStatsWidget(StatsWidget):

    def __init__(self, parent=None):
        super(RenderNodeStatsWidget, self).__init__(parent)
        rh = RequestHandler()
        rh.renderNodesStatsChanged.connect(self.onStatsChanged)
