"""
Requests module. All requests are handled here.
"""


import json
import requests

from pydantic import (
    HttpUrl,
    SecretStr,
)
from pydantic.dataclasses import dataclass

from . import models
from . import utils
from .logger import get_logger


logger = get_logger("requests")


@dataclass
class Request():
    """
    Base class for all HTTP requests.

    Args:
        api_key: The authentication API key for API calls.
        base_path: PeopleDataLabs' API base URL.
        type_: The type of API to call.
        endpoint: The endpoint of the API to call.
        params: The parameters to use in the API call.
    """
    api_key: SecretStr
    base_path: HttpUrl
    type_: str
    endpoint: str
    params: models.EnrichmentModel

    def get(self):
        """
        Exceutes a GET request from the specified API.

        Args:
            kwargs: Parameters for the API.

        Returns:
            A requests.Response object with the result of the HTTP call.
        """
        params = {
            param: value for param, value in self.params if value is not None
        }
        params["api_key"] = self.api_key
        url = f"{self.base_path}/{self.type_}/{self.endpoint}"
        logger.debug(
            "Calling %s/%s with params: %s",
            self.base_path,
            self.type_,
            json.dumps(params, indent=2, default=utils.json_defaults)
        )
        params["api_key"] = params["api_key"].get_secret_value()
        response = requests.get(url, params=params)

        return response.json()
