"""
Utility scripts which do not strictly belong to any other module.
"""


from pydantic import (
    SecretStr
)


def json_defaults(value):
    """
    JSON default callback to serialize different types of data.
    """
    mapping = {
        SecretStr: str
    }
    return mapping[type(value)](value)
