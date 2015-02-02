from PyQt4.QtGui import QAction
from pulimonitor.util.user import currentUser


class Action(QAction):
    '''
    A custom QAction class, which allows to set a category (e.g. "Jobs" or
    "Rendernode"), an ID and a selection sensitiveness.
    The category can be used to group actions in a interface.
    The ID is used to allow actions to be associated with "roles" a "user" can
    have.
    Selection sensitiveness means that the action is dependent on a selection
    and only enabled on if the selection is valid.
    '''

    def __init__(self, text, category, aId, selectionSensitive, parent):
        super(Action, self).__init__(text, parent)
        '''
        :param text: text displayed for action
        :type text: str
        :param category: category used for grouping an action in the user
        permission dialog
        :type category: str
        :param aId: an ID which uniquely identifies the action
        :type aId: int
        :param selectionSensitive: is this action selection sensitive?
        :type selectionSensitive: bool
        :param parent: parent Qt object
        :type parent: QObject
        '''
        self.id = aId
        self.category = category
        self.selectionSensitive = selectionSensitive
        self.isAllowed = self.id in currentUser().allowedActions()
        self.setEnabled(self.isAllowed and not self.selectionSensitive)

    def setEnabled(self, value):
        '''
        Only allow actions to be enabled if the user is allowed to use them.
        Otherwise they will always be set to disabled.
        :param value: indicating the status of the action
        :type value: bool
        '''
        if self.isAllowed:
            return QAction.setEnabled(self, value)
        else:
            return QAction.setEnabled(self, False)

    def setEnabledOnSelectionChange(self, value):
        '''
        Special version of "setEnabled" taking the selection sensitivity" into
        account.
        :param value: indicating the status of the action
        :type value: bool
        '''
        if self.selectionSensitive:
            self.setEnabled(value)
        else:
            self.setEnabled(True)
