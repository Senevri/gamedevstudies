import logging


def getLogger(name: str, file: str = "root", loglevel=None):
    name = name or __name__
    loglevel = loglevel or logging.DEBUG
    logging.basicConfig()
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.warn = logger.warning
    return logger
