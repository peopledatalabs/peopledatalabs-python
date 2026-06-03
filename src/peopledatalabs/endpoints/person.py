"""
Defines all API endpoints for the 'Person' section.
"""

from pydantic import StrictStr, validate_call
from pydantic.dataclasses import dataclass

from .. import models
from ..logger import get_logger
from ..models import person as person_models
from . import Endpoint

logger = get_logger("endpoints.person")


@dataclass
class Person(Endpoint):
    """
    Class for all APIs of "person" type.
    """

    section: str = "person"

    def bulk(self, **kwargs):
        """
        Calls PeopleDataLabs' person/bulk enrichment API.
        https://docs.peopledatalabs.com/docs/bulk-enrichment-api.

        Args:
            **kwargs: Parameters for the API as defined
                in the documentation.

        Returns:
            A requests.Response object with the result of the HTTP call.
        """
        return self._bulk(person_models.BulkModel, **kwargs)

    def enrichment(self, **kwargs):
        """
        Calls PeopleDataLabs' person/enrich API.
        https://docs.peopledatalabs.com/docs/enrichment-api.

        Args:
            **kwargs: Parameters for the API as defined
                in the documentation.

        Returns:
            A requests.Response object with the result of the HTTP call.
        """
        return self._enrichment(person_models.EnrichmentModel, **kwargs)

    def identify(self, **kwargs):
        """
        Calls PeopleDataLabs' person/identify API.
        https://docs.peopledatalabs.com/docs/identify-api.

        Args:
            **kwargs: Parameters for the API as defined
                in the documentation.

        Returns:
            A requests.Response object with the result of the HTTP call.
        """
        return self._identify(person_models.IdentifyModel, **kwargs)

    @validate_call
    def retrieve(self, person_id: StrictStr, **kwargs):
        """
        Calls PeopleDataLabs' person/retrieve API.
        https://docs.peopledatalabs.com/docs/person-retrieve-api.

        Args:
            person_id (str): The person's ID from the
                People Data Labs dataset;
            **kwargs: Additional parameters for the API as defined
                in the documentation.

        Returns:
            A requests.Response object with the result of the HTTP call.
        """
        return self._retrieve(models.BaseRequestModel, person_id, **kwargs)

    def search(self, **kwargs):
        """
        Calls PeopleDataLabs' person/search API.
        https://docs.peopledatalabs.com/docs/search-api.

        Args:
            **kwargs: Parameters for the API as defined
                in the documentation.

        Returns:
            A requests.Response object with the result of the HTTP call.
        """
        return self._search(person_models.SearchModel, **kwargs)

    def changelog(self, **kwargs):
        """
        Calls PeopleDataLabs' person/changelog API.
        https://docs.peopledatalabs.com/docs/person-changelog-api.

        Args:
            **kwargs: Parameters for the API as defined
                in the documentation.

        Returns:
            A requests.Response object with the result of the HTTP call.
        """
        return self._changelog(person_models.ChangelogModel, **kwargs)
