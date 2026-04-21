"""
Defines all API endpoints for the 'Job Posting' section.
"""

from pydantic.v1.dataclasses import dataclass

from . import Endpoint
from ..models import job_posting as job_posting_models
from ..logger import get_logger


logger = get_logger("endpoints.job_posting")


@dataclass
class JobPosting(Endpoint):
    """
    Class for all APIs of "job_posting" type.
    """

    section: str = "job_posting"

    def search(self, **kwargs):
        """
        Calls PeopleDataLabs' job_posting/search API.

        Dispatches to the Elasticsearch-style validator when 'query' is
        provided, and to the field-based validator otherwise.

        Args:
            **kwargs: Parameters for the API as defined
                in the documentation.

        Returns:
            A requests.Response object with the result of the HTTP call.
        """
        if "query" in kwargs:
            model = job_posting_models.JobPostingQuerySearchModel
        else:
            model = job_posting_models.JobPostingParamSearchModel
        return self._search(model, **kwargs)
