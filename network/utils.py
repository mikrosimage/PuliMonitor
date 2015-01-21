import requests

from util.config import Config


def testConnectivity():
    '''
    This function tries to connect to the server configured in settings.ini
    :returns: boolean -- True if connection was successfull, else False
    '''
    config = Config()
    url = "http://{host}:{port}/pools".format(host=config.hostname, port=config.port)
    try:
        requests.get(url)
        return True
    except:
        return False
