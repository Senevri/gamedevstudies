import logging

def getLogger(name:str, loglevel=None):
    name = name or __name__
    loglevel = loglevel or logging.DEBUG
    logging.basicConfig()
    logger = logging.getLogger(name)
    logging.getLogger(name).setLevel(logging.DEBUG)
    logger.warn = logger.warning
    return logger
