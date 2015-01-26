import os
import sys


CONFIG_DIR = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "config")
GENERAL_CONFIG_PATH = os.path.join(CONFIG_DIR, 'general.ini')
LOG_CONFIG_PATH = os.path.join(CONFIG_DIR, 'logging.ini')
FILTER_CONFIG_DIR = os.path.join(CONFIG_DIR, "filters")


def listfiles(path, ext=None):
    result = []
    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f)):
            if (ext and f.endswith(ext)) or (not ext):
                result.append(f)
    return result
