"""
Defines all API endpoints for the 'Company' section.
"""

from pydantic.v1.dataclasses import dataclass

from . import Endpoint
from ..models import company as company_models
from ..logger import get_logger


logger = get_logger("company")


@dataclass
class Company(Endpoint):
    """
    Class for all APIs of "company" type.
    """

    section: str = "company"

    def enrichment(self, **kwargs):
        """
        Calls PeopleDataLabs' company/enrich API.
        https://docs.peopledatalabs.com/docs/company-enrichment-api.

        Args:
            **kwargs: Parameters for the API as defined
                in the documentation.

        Returns:
            A requests.Response object with the result of the HTTP call.
        """
        return self._enrichment(company_models.EnrichmentModel, **kwargs)

    def bulk(self, **kwargs):
        """
        Calls PeopleDataLabs' company bulk enrichment API.
        https://docs.peopledatalabs.com/docs/bulk-company-enrichment-api.

        Args:
            **kwargs: Parameters for the API as defined
                in the documentation.

        Returns:
            A requests.Response object with the result of the HTTP call.
        """
        return self._company_bulk(company_models.CompanyBulkModel, **kwargs)

    def search(self, **kwargs):
        """
        Calls PeopleDataLabs' company/search API.
        https://docs.peopledatalabs.com/docs/company-search-api.

        Args:
            **kwargs: Parameters for the API as defined
                in the documentation.

        Returns:
            A requests.Response object with the result of the HTTP call.
        """
        return self._search(company_models.SearchModel, **kwargs)

    def cleaner(self, **kwargs):
        """
        Calls PeopleDataLabs' company/clean API.

        Args:
            **kwargs: Parameters for the API as defined
                in the documentation.

        Returns:
            A requests.Response object with the result of the HTTP call.
        """
        return self._cleaner(company_models.CleanerModel, **kwargs)
