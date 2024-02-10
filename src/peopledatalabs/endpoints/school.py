"""
Defines all API endpoints for the 'School' section.
"""

from pydantic.v1.dataclasses import dataclass

from . import Endpoint
from ..logger import get_logger
from ..models import school as school_models


logger = get_logger("endpoints.school")


@dataclass
class School(Endpoint):
    """
    Class for all APIs of "school" type.
    """

    section: str = "school"

    def cleaner(self, **kwargs):
        """
        Calls PeopleDataLabs' school/clean API.

        Args:
            **kwargs: Parameters for the API as defined
                in the documentation.

        Returns:
            A requests.Response object with the result of the HTTP call.
        """
        return self._cleaner(school_models.CleanerModel, **kwargs)
