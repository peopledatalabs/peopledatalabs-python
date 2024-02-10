"""
Defines all API endpoints for the 'Location' section.
"""

from pydantic.v1.dataclasses import dataclass

from . import Endpoint
from ..logger import get_logger
from ..models import location as location_models


logger = get_logger("endpoints.location")


@dataclass
class Location(Endpoint):
    """
    Class for all APIs of "location" type.
    """

    section: str = "location"

    def cleaner(self, **kwargs):
        """
        Calls PeopleDataLabs' location/clean API.

        Args:
            **kwargs: Parameters for the API as defined
                in the documentation.

        Returns:
            A requests.Response object with the result of the HTTP call.
        """
        return self._cleaner(location_models.CleanerModel, **kwargs)
