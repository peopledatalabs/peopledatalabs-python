"""
Logging utility module to invoke different children of the same root logger,
from different modules (and tests).
"""

import logging

from .settings import settings


logging.basicConfig(format=settings.log_format, style="{")


def get_logger(name: str = None, log_level: str = settings.log_level):
    """
    Utility function to retrieve a logger.

    Args:
        name (:obj:`str`, optional): Specify a name if you want
            to retrieve a logger which is a child of
            PeopleDataLabs logger.
        log_level (:obj:`str`, optional): Specify the log level
            for this particular logger.

    Returns:
        The PeopleDataLabs logger, or one of its children.
    """
    default = "PeopleDataLabs"
    if name:
        logger = logging.getLogger(f"{default}.{name}")
    else:
        logger = logging.getLogger(default)

    if log_level is not None:
        logger.setLevel(log_level)
    logger.debug("Got logger %s", logger)

    return logger
