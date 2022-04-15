"""
Requests module. All requests are handled here.
"""


import json
import requests
from typing import Dict

from pydantic import (
    HttpUrl,
    SecretStr,
)
from pydantic.dataclasses import dataclass

from . import models
from . import utils
from .logger import get_logger


logger = get_logger("requests")

request_models_map = {
    "person": {
        "enrich": models.PersonEnrichmentModel
    }
}


@dataclass
class Request():
    """
    Base class for all HTTP requests.

    Args:
        api_key: The authentication API key for API calls.
        base_path: PeopleDataLabs' API base URL.
        section: The type of API to call.
        endpoint: The endpoint of the API to call.
        params: The parameters to use in the API call.
    """
    api_key: SecretStr
    base_path: HttpUrl
    section: str
    endpoint: str
    headers: Dict[str, str]
    params: dict

    def __post_init__(self):
        """
        Refactors self.params, validating per endpoint
        and stripping off None values.
        Also defines self.url which is the result of
        base_path + section (if any) + endpoint.
        """
        model = request_models_map[self.section][self.endpoint]
        params = model(**self.params).dict()
        self.params = {
            param: value for param, value in params.items()
            if value is not None
        }
        self.params["api_key"] = self.api_key
        logger.debug(
            "Calling %s/%s with params: %s",
            self.base_path,
            self.section,
            json.dumps(self.params, indent=2, default=utils.json_defaults)
        )
        self.params["api_key"] = self.params["api_key"].get_secret_value()

        self.url = self.base_path
        if self.section:
            self.url += "/" + self.section
        self.url += "/" + self.endpoint

    def get(self):
        """
        Exceutes a GET request from the specified API.

        Returns:
            A requests.Response object with the result of the HTTP call.
        """
        return requests.get(self.url, params=self.params)
