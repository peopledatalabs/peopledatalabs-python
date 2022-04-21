"""
Utility scripts which do not strictly belong to any other module.
"""


import functools

from pydantic import SecretStr

from .errors import EmptyParametersException


def check_empty_parameters(func):
    """
    Decorator for API request methods which checks if parameters are empty.
    """

    @functools.wraps(func)
    def _check(ref, *args, **kwargs):
        if not kwargs:
            raise EmptyParametersException
        return func(ref, *args, **kwargs)

    return _check


def json_defaults(value):
    """
    JSON default callback to serialize different types of data.
    """
    mapping = {SecretStr: str}
    return mapping[type(value)](value)
