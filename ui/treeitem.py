

class TreeItem(object):

    def __init__(self, data, parent):
        self.parent = parent
        self.data = data
        self.childItems = []
        self.childItemLookup = {}
        if parent:
            self.parent.appendChild(self)

    def findChild(self, key):
        return self.childItemLookup.get(key)

    def appendChild(self, item):
        self.childItemLookup[item.data["id"]] = item
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        print len(self.childItems)
        return len(self.childItems)

    def row(self):
        if self.parent:
            return self.parent.childItems.index(self)
        return 0

    def isRoot(self):
        return self.parent is None

    def deleteChild(self, row):
        del self.childItems[row]
        del self.childItemLookup[self.childItems[row]["id"]]

    def __repr__(self, *args, **kwargs):
        return "%s(%s)" % (self.__class__.__name__, repr(self.data))

    def delete(self):
        self.parent.childItems.remove(self)
        del self.parent.childItemLookup[self.data["id"]]
        self.parent = None
