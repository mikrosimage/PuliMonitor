'''
Created on Jan 27, 2015

@author: Sebastian Elsner
@organization: rise|fx GmbH
'''
from ui.stats import StatsWidget
from network.requesthandler import getRequestHandler


class RenderNodeStatsWidget(StatsWidget):

    def __init__(self, parent=None):
        super(RenderNodeStatsWidget, self).__init__(parent)
        rh = getRequestHandler()
        rh.renderNodesStatsChanged.connect(self.onStatsChanged)
