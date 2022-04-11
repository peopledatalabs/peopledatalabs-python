import logging


logging.basicConfig()


def get_logger(name: str = None):
    default = "PeopleDataLabs"
    if name:
        logger = logging.getLogger(f"{default}.{name}")
    else:
        logger = logging.getLogger(default)

    logger.debug(f"Got logger {logger}")

    return logger
