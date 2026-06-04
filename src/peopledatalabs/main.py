"""
Client's main module.
"""

from typing import Annotated

from pydantic import Field, field_validator
from pydantic.dataclasses import dataclass

from .endpoints import Endpoint
from .endpoints.company import Company
from .endpoints.job_posting import JobPosting
from .endpoints.location import Location
from .endpoints.person import Person
from .endpoints.school import School
from .logger import get_logger
from .models import AutocompleteModel, IPModel, JobTitleModel
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

    api_key: str | None = Field(
        default=settings.api_key, validate_default=True
    )
    base_path: Annotated[str, Field(pattern=r"^https?://")] | None = None
    version: Annotated[str, Field(pattern=settings.version_re)] = (
        settings.version
    )
    log_level: str = None
    sandbox: bool = False

    @field_validator("api_key", mode="before")
    @classmethod
    def api_key_not_none(cls, v):
        """
        Checks an API key is passed to the Client object.
        """
        if v is None:
            raise ValueError("Please enter a value for API key.")
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
        if self.sandbox:
            self.base_path = settings.sandbox_base_path + self.version

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
                "Content-Type": "application/json",
                "User-Agent": "PDL-PYTHON-SDK",
                "SDK-Version": settings.sdk_version,
            },
            params=kwargs,
            validator=AutocompleteModel,
        ).get()

    @check_empty_parameters
    def job_title(self, **kwargs):
        """
        Calls PeopleDataLabs' job_title API.

        Args:
            **kwargs: Parameters for the API as defined
                in the documentation.

        Returns:
            A requests.Response object with the result of the HTTP call.
        """
        url = Endpoint(self.api_key, self.base_path).get_url(
            endpoint="job_title/enrich"
        )
        return Request(
            api_key=self.api_key,
            url=url,
            headers={
                "Accept-Encoding": "gzip",
                "Content-Type": "application/json",
                "User-Agent": "PDL-PYTHON-SDK",
                "SDK-Version": settings.sdk_version,
            },
            params=kwargs,
            validator=JobTitleModel,
        ).get()

    @check_empty_parameters
    def ip(self, **kwargs):
        """
        Calls PeopleDataLabs' IP Enrichment API.

        Args:
            **kwargs: Parameters for the API as defined
                in the documentation.

        Returns:
            A requests.Response object with the result of the HTTP call.
        """
        url = Endpoint(self.api_key, self.base_path).get_url(
            endpoint="ip/enrich"
        )
        return Request(
            api_key=self.api_key,
            url=url,
            headers={
                "Accept-Encoding": "gzip",
                "Content-Type": "application/json",
                "User-Agent": "PDL-PYTHON-SDK",
                "SDK-Version": settings.sdk_version,
            },
            params=kwargs,
            validator=IPModel,
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

    @property
    def job_posting(self):
        """
        Calls API from the job_posting section.
        """
        return JobPosting(self.api_key, self.base_path)
