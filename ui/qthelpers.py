import sip


def setSipApiVersion(version):
    '''
    Set the Sip api to the given version.
    :param version: version to use
    :type version: int
    '''
    for apitype in ['QString', 'QVariant', 'QDate', 'QDateTime', 'QTextStream', 'QTime', 'QUrl']:
        sip.setapi(apitype, version)
