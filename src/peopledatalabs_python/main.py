"""
Client's main module.
"""


import functools

from pydantic import (
    HttpUrl,
    SecretStr,
    StrictStr,
    constr,
    validate_arguments,
)
from pydantic.dataclasses import dataclass

from . import models
from .errors import EmptyParametersException
from .logger import get_logger
from .requests import Request
from .settings import settings


logger = get_logger()


def check_empty_parameters(func):
    """
    Decorator for API request methods which checks if parameters are empty.
    """
    @functools.wraps(func)
    def _check(ref, **kwargs):
        if not kwargs:
            raise EmptyParametersException
        return func(ref, **kwargs)
    return _check


@dataclass
class PDLPY():
    """
    Client's main class.
    All methods derive from the instantiation of this class.

    Args:
        api_key: The authentication API key for API calls.
        base_path: PeopleDataLabs' API base URL, with version.
        version: PeopleDataLabs' API version to call. Will be used only if
            base_path has no value.
    """
    api_key: SecretStr = settings.api_key
    base_path: HttpUrl = None
    version: constr(regex=settings.version_re) = settings.version
    log_level: str = None

    def __post_init__(self):
        """
        Sets the actual base_path and sets log_level globally across modules.
        """
        if self.base_path is None:
            self.base_path = settings.base_path + self.version
        if self.log_level is not None:
            settings.log_level = self.log_level
            logger.setLevel(self.log_level)

        self.person = Person(self.api_key, self.base_path)


@dataclass
class Endpoint():
    """
    Base class for all endpoints.

    Args:
        api_key: The authentication API key for API calls.
        base_path: PeopleDataLabs' API base URL.
    """
    api_key: SecretStr
    base_path: HttpUrl

    def _get_url(self, endpoint: str, section: str = None):
        url = self.base_path
        if section:
            url += "/" + section
        url += "/" + endpoint

        return url


@dataclass
class Person(Endpoint):
    """
    Class for all APIs of "person" type.
    """

    @check_empty_parameters
    def bulk(self, **kwargs):
        """
        Calls PeopleDataLabs' bulk enrichment API.

        Args:
            kwargs: Parameters for the API as defined in the documentation.

        Returns:
            A requests.Response object with the result of the HTTP call.
        """
        url = self._get_url(section="person", endpoint="bulk")
        return Request(
            api_key=self.api_key,
            url=url,
            headers={"Content-Type": "application/json"},
            params=kwargs,
            validator=models.PersonBulkModel
        ).post()

    @check_empty_parameters
    def enrichment(self, **kwargs):
        """
        Calls PeopleDataLabs' enrichment API.

        Args:
            kwargs: Parameters for the API as defined in the documentation.

        Returns:
            A requests.Response object with the result of the HTTP call.
        """
        url = self._get_url(section="person", endpoint="enrich")
        return Request(
            api_key=self.api_key,
            url=url,
            headers={"Accept-Encoding": "gzip"},
            params=kwargs,
            validator=models.PersonEnrichmentModel
        ).get()

    @validate_arguments
    def retrieve(self, person_id: StrictStr, **kwargs):
        """
        Calls PeopleDataLabs' enrichment API.

        Args:
            kwargs: Parameters for the API as defined in the documentation.

        Returns:
            A requests.Response object with the result of the HTTP call.
        """
        url = self._get_url(section="person", endpoint="retrieve")
        url += "/" + person_id
        return Request(
            api_key=self.api_key,
            url=url,
            headers={"Accept-Encoding": "gzip"},
            params=kwargs,
            validator=models.BaseRequestModel
        ).get()
