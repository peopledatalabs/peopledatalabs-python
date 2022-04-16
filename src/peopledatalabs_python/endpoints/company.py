"""
Defines all API endpoints for the 'Company' section.
"""


from pydantic.dataclasses import dataclass

from . import Endpoint
from ..models import company as company_models
from ..logger import get_logger
from ..requests import Request
from ..utils import check_empty_parameters


logger = get_logger("company")


@dataclass
class Company(Endpoint):
    """
    Class for all APIs of "company" type.
    """
    section: str = "company"

    @check_empty_parameters
    def enrichment(self, **kwargs):
        """
        Calls PeopleDataLabs' enrichment API.
        https://docs.peopledatalabs.com/docs/company-enrichment-api

        Args:
            **kwargs: Parameters for the API as defined
                in the documentation.

        Returns:
            A requests.Response object with the result of the HTTP call.
        """
        url = self._get_url(endpoint="enrich")
        return Request(
            api_key=self.api_key,
            url=url,
            headers={"Accept-Encoding": "gzip"},
            params=kwargs,
            validator=company_models.EnrichmentModel
        ).get()
