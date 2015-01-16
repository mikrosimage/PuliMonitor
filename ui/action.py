from PyQt4.QtGui import QAction


class Action(QAction):
    '''
    A custom QAction class, which allows to set a category for an action (e.g.
    "Jobs" or "Rendernode") and a required user role for this action to
    be accessible.'''

    def __init__(self, *args, **kwargs):
        super(Action, self).__init__(*args, **kwargs)
        self.id = None
        self.category = None
