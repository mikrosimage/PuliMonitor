from collections import defaultdict

import requests

from pulimonitor.util.config import Config


def testServerConnectivity():
    '''
    This function tries to connect to the server configured in settings.ini
    :returns: boolean -- True if connection was successfull, else False
    '''
    config = Config()
    connectivity = defaultdict(list)
    for hostname, port in config.items("Servers"):
        url = "http://{host}:{port}/pools".format(host=hostname, port=port)
        try:
            requests.get(url)
            connectivity["online"].append((hostname, port))
        except:
            connectivity["offline"].append((hostname, port))
    return connectivity
