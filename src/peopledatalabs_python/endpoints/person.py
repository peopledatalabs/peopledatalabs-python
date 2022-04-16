"""
Defines all API endpoints for the 'Person' section.
"""


from pydantic import (
    StrictStr,
    validate_arguments,
)
from pydantic.dataclasses import dataclass

from . import Endpoint
from .. import models
from ..logger import get_logger
from ..requests import Request
from ..utils import check_empty_parameters


logger = get_logger("person")


@dataclass
class Person(Endpoint):
    """
    Class for all APIs of "person" type.
    """
    section: str = "person"

    @check_empty_parameters
    def bulk(self, **kwargs):
        """
        Calls PeopleDataLabs' bulk enrichment API.

        Args:
            kwargs: Parameters for the API as defined in the documentation.

        Returns:
            A requests.Response object with the result of the HTTP call.
        """
        url = self._get_url(endpoint="bulk")
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
        url = self._get_url(endpoint="enrich")
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
        Calls PeopleDataLabs' retrieve API.

        Args:
            person_id: The person's ID from the People Data Labs dataset;
            kwargs: Parameters for the API as defined in the documentation.

        Returns:
            A requests.Response object with the result of the HTTP call.
        """
        url = self._get_url(endpoint="retrieve")
        url += "/" + person_id
        return Request(
            api_key=self.api_key,
            url=url,
            headers={"Accept-Encoding": "gzip"},
            params=kwargs,
            validator=models.BaseRequestModel
        ).get()

    @check_empty_parameters
    def search(self, **kwargs):
        """
        Calls PeopleDataLabs' search API.

        Args:
            kwargs: Parameters for the API as defined in the documentation.

        Returns:
            A requests.Response object with the result of the HTTP call.
        """
        url = self._get_url(endpoint="search")
        return Request(
            api_key=self.api_key,
            url=url,
            headers={
                "Content-Type": "application/json",
                "Accept-Encoding": "gzip",
            },
            params=kwargs,
            validator=models.PersonSearchModel
        ).post()
