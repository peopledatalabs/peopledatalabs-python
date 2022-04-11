import functools

from pydantic import Field, HttpUrl, SecretStr, validate_arguments

from . import schemas
from .defaults import Defaults
from .errors import EmptyParametersException
from .logger import get_logger


logger = get_logger()


def check_empty_parameters(func):
    @functools.wraps(func)
    def _check(ref, **kwargs):
        if not kwargs:
            raise EmptyParametersException
        else:
            return func(ref, **kwargs)
    return _check


class PDLPY():
    @validate_arguments
    def __init__(
        self,
        api_key: SecretStr,
        base_path: HttpUrl = None,
        version: str = Field(default=None, regex="v[0-9]"),
    ):
        self.api_key = api_key
        version = version if version else Defaults.version
        self.base_path = self._make_base_path(base_path, version)
        self.person = Person(self.api_key, self.base_path)

    def _make_base_path(self, base_path: str, version: str):
        _base_path = Defaults.base_path
        if base_path is not None:
            _base_path = base_path + version

        return _base_path


class Person(PDLPY):
    def __init__(self, api_key: str, base_path: str):
        self.api_key = api_key
        self.base_path = base_path

    @check_empty_parameters
    def enrichment(self, **kwargs):
        params = schemas.Person(**kwargs)
        return params
