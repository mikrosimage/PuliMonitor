import os
import sys


def listfiles(path, ext=None):
    result = []
    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f)):
            if (ext and f.endswith(ext)) or (not ext):
                result.append(f)
    return result


def cdUp(path, times=1):
    result = path
    for _time in range(times):
        result = os.path.abspath(os.path.join(result, os.pardir))
    return result

CONFIG_DIR = os.path.join(cdUp(sys.argv[0], 2), "config")
GENERAL_CONFIG_PATH = os.path.join(CONFIG_DIR, 'general.ini')
LOG_CONFIG_PATH = os.path.join(CONFIG_DIR, 'logging.ini')
FILTER_CONFIG_DIR = os.path.join(CONFIG_DIR, "filters")
