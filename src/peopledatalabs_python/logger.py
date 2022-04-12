import logging

from .settings import settings


logging.basicConfig(format=settings.log_format, style="{")


def get_logger(name: str = None, log_level: str = settings.log_level):
    default = "PeopleDataLabs"
    if name:
        logger = logging.getLogger(f"{default}.{name}")
    else:
        logger = logging.getLogger(default)

    if log_level is not None:
        logger.setLevel(log_level)
    logger.debug("Got logger %s", logger)

    return logger
