from PyQt4.QtCore import Qt


class TreeItem(object):

    def __init__(self, data, parent):
        self.parent = parent
        self._data = data
        self.childItems = []
        self._childCount = 0
        self._row = 0
        if parent:
            self.parent.appendChild(self)

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def appendChild(self, item):
        item._row = self._childCount
        self._childCount += 1
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return self._childCount

    def row(self):
        return self._row

    def deleteChild(self, row):
        del self.childItems[row]

    def __repr__(self, *args, **kwargs):
        return "%s(%s)" % (self.__class__.__name__, repr(self._data)) + str(self.parent)

    def dump(self, indent=""):
        print indent + str(self)
        for c in self.childItems:
            c.dump(indent + "    ")

    def delete(self):
        self.parent.childItems.remove(self)
        self.parent = None
