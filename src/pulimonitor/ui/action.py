from PyQt4.QtGui import QAction
from pulimonitor.util.user import currentUser


class Action(QAction):
    '''
    A custom QAction class, which allows to set a category for an action (e.g.
    "Jobs" or "Rendernode") and a required user role for this action to
    be accessible.'''

    def __init__(self, text, category, aId, parent):
        super(Action, self).__init__(text, parent)
        '''
        :param text: text displayed for action
        :type text: str
        :param category: category used for grouping an action in the user
        permission dialog
        :type category: str
        :param aId: an ID which uniqualy identifies the action
        :type aId: int
        :param parent: parent Qt object
        :type parent: QObject
        '''
        self.id = aId
        self.category = category
        self.setEnabled(self.id in currentUser().allowedActions())
