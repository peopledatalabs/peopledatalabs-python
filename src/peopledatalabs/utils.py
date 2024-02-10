"""
Utility scripts which do not strictly belong to any other module.
"""

import functools

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
