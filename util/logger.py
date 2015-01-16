import logging


def setupConsoleLogger(logger=logging.root):
    '''
    Sets up a basic console logger.
    :param logger: the logger to setup, defaults to root
    :type logger: logging.Logger
    '''

    handler = logging.StreamHandler()
    handler.setFormatter(standardFormatter())
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


def setupFileLogger(logger=logging.root):
    '''
    Sets up a basic file logger.
    :param logger: the logger to setup, defaults to root
    :type logger: logging.Logger
    '''

    handler = logging.FileHandler("pulimonitor.log")
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(standardFormatter())
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    return logger


def standardFormatter():
    '''
    Returns a standard formatter for logging
    '''

    return logging.Formatter('%(asctime)-6s - %(name)s - '
                             '%(levelname)s - %(message)s',
                             '%Y-%m-%d %H:%M:%S')
