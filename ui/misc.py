'''
Created on Jan 27, 2015

@author: Sebastian Elsner
@organization: rise|fx GmbH
'''

from PyQt4.QtGui import QFrame


def VLine(parent=None):
    f = QFrame(parent)
    f.setFrameShape(QFrame.VLine)
    f.setFrameShadow(QFrame.Sunken)
    return f
