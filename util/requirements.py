
import imp
import logging


def fulfilled():
    log = logging.getLogger()
    res = True
    try:
        imp.find_module('requests')
    except:
        log.error("Requests library missing")
        res = False

    try:
        imp.find_module('PyQt4')
    except:
        log.error("PyQt4 library missing")
        res = False

    try:
        imp.find_module('sip')
    except:
        log.error("Sip library missing")
        res = False

    try:
        imp.find_module('octopus')
    except:
        log.error("Puli octopus library missing")
        res = False

    if not res:
        log.error("Please make sure these libraries are installed "
                  "and in your PYTHONPATH")

    return res
