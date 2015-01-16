
import logging


def fulfilled():
    log = logging.getLogger()
    res = True
    try:
        import requests  # @UnusedImport
    except:
        log.error("Requests library missing")
        res = False

    try:
        import PyQt4  # @UnusedImport
    except:
        log.error("PyQt4 library missing")
        res = False

    try:
        import sip  # @UnusedImport
    except:
        log.error("Sip library missing")
        res = False

    try:
        import octopus  # @UnusedImport
    except:
        log.error("Puli octopus library missing")
        res = False

    if res:
        log.error("Please make sure these libraries are in your PYTHONPATH")

    return res
