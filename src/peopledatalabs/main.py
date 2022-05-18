"""
Client's main module.
"""


from pydantic import (
    HttpUrl,
    SecretStr,
    constr,
    validator,
)
from pydantic.dataclasses import dataclass


from .endpoints import Endpoint
from .endpoints.person import Person
from .endpoints.company import Company
from .endpoints.location import Location
from .endpoints.school import School
from .logger import get_logger
from .models import AutocompleteModel
from .requests import Request
from .settings import settings
from .utils import check_empty_parameters


logger = get_logger()


@dataclass
class PDLPY:
    """
    Client's main class. All methods derive from the instantiation of this
    class.

    Args:
        api_key (:obj:`str`, optional): The authentication
            API key for API calls.
        base_path (:obj:`str`, optional): PeopleDataLabs' API base URL.
        version (:obj:`str`, optional): PeopleDataLabs' API version.
            Will be used only if base_path has no value.
        log_level (:obj:`str`, optional): The logger level.
    """

    api_key: SecretStr = settings.api_key
    base_path: HttpUrl = None
    version: constr(regex=settings.version_re) = settings.version
    log_level: str = None

    @validator("api_key", pre=True, always=True)
    def api_key_not_none(cls, v):
        """
        Checks an API key is passed to the Client object.
        """
        if v is None:
            raise ValueError(
                "Please enter a value for API key, or define it either in"
                " your environment or .env file as PDL_API_KEY"
            )
        return v

    def __post_init__(self):
        """
        Sets the actual base_path and sets log_level globally across modules.
        """
        if self.base_path is None:
            self.base_path = settings.base_path + self.version
        if self.log_level is not None:
            settings.log_level = self.log_level
            logger.setLevel(self.log_level)

    @check_empty_parameters
    def autocomplete(self, **kwargs):
        """
        Calls PeopleDataLabs' autocomplete API.

        Args:
            **kwargs: Parameters for the API as defined
                in the documentation.

        Returns:
            A requests.Response object with the result of the HTTP call.
        """
        url = Endpoint(self.api_key, self.base_path).get_url(
            endpoint="autocomplete"
        )
        return Request(
            api_key=self.api_key,
            url=url,
            headers={
                "Accept-Encoding": "gzip",
                "User-Agent": "PDL-PYTHON-SDK",
                "Content-Type": "application/json",
            },
            params=kwargs,
            validator=AutocompleteModel,
        ).get()

    @property
    def company(self):
        """
        Calls API from the company section.
        """
        return Company(self.api_key, self.base_path)

    @property
    def location(self):
        """
        Calls API from the location section.
        """
        return Location(self.api_key, self.base_path)

    @property
    def school(self):
        """
        Calls API from the school section.
        """
        return School(self.api_key, self.base_path)

    @property
    def person(self):
        """
        Calls API from the person section.
        """
        return Person(self.api_key, self.base_path)
