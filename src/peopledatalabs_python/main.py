import functools

from pydantic import (
    HttpUrl,
    SecretStr,
    constr,
)
from pydantic.dataclasses import dataclass

from .errors import EmptyParametersException
from .logger import get_logger
from .requests import Request
from .settings import settings


logger = get_logger()


def check_empty_parameters(func):
    @functools.wraps(func)
    def _check(ref, **kwargs):
        if not kwargs:
            raise EmptyParametersException
        return func(ref, **kwargs)
    return _check


@dataclass
class PDLPY():
    api_key: SecretStr = settings.api_key
    base_path: HttpUrl = None
    version: constr(regex=settings.version_re) = "v5"
    log_level: str = None

    def __post_init__(self):
        if self.base_path is None:
            self.base_path = settings.base_path + self.version
        if self.log_level is not None:
            settings.log_level = self.log_level
            logger.setLevel(self.log_level)

        self.person = Person(self.api_key, self.base_path)


@dataclass
class Endpoint():
    api_key: SecretStr
    base_path: HttpUrl


@dataclass
class Person(Endpoint):
    @check_empty_parameters
    def enrichment(self, **kwargs):
        return Request(
            api_key=self.api_key,
            base_path=self.base_path,
            type_="person",
            endpoint="enrich",
            params=kwargs
        ).get()
