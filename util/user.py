"""
Basic RBAC implementation. The User and Role can be used with any backend
(file storage, database)
"""


class User(object):
    '''
    Class representing a user. Provides an interface to assign roles to a user
    and query the permissions granted to that Role.
    '''

    def __init__(self, name):
        self.name = name
        self.roles = []

    def allowedActions(self):
        '''
        Returns a list of all Action IDs included in any role the user
        was assigned to.
        '''
        # TODO: we could cache this with a cached_property decorator
        actions = set()
        for role in self.roles:
            actions.update(role.actions)
        return actions

    def __repr__(self, *args, **kwargs):
        return "User({0}, {1})".format(self.name, self.roles)


class Role(object):
    '''
    Class representing a role with permission object like Actions assignable.
    '''

    def __init__(self, name, actions):
        self.name = name
        self.actions = actions

    def __repr__(self, *args, **kwargs):
        return "Role({0})".format(self.name)


# Storage for currently logged in user
CURRENT_USER = None


def currentUser():
    '''
    Returns the currently logged in User.
    '''
    return CURRENT_USER


def loginUser(name):
    '''
    Logs in a user with a specific user.
    :param name: user name
    :type name: str
    '''
    global CURRENT_USER
    CURRENT_USER = User(name)
    # This is just a temp hack to assign a role to an user without
    # an actual backend
    CURRENT_USER.roles.append(Role("Admin", [9, 10]))
