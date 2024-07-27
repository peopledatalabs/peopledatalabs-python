"""
Requests module.

All requests are handled here.
"""

import json
from typing import Dict, Type

from pydantic.v1 import (
    BaseModel,
    HttpUrl,
)
from pydantic.v1.dataclasses import dataclass
import requests

from .logger import get_logger


logger = get_logger("requests")


@dataclass
class Request:
    """
    Base class for all HTTP requests.

    Args:
        api_key (str): The authentication API key for API calls.
        url (str): URL of the API to call.
        headers (dict of str: str): The request headers.
        params (dict): The parameters to use in the API call.
        validator: The validator to use to validate params.
    """

    api_key: str
    url: HttpUrl
    headers: Dict[str, str]
    params: dict
    validator: Type[BaseModel]

    def __post_init__(self):
        """
        Validates self.params using the validator received in self.validator.
        """
        logger.debug("Request object received params: %s", self.params)
        self.params = self.validator(**self.params).dict(exclude_none=True)
        logger.debug("Request object params after validation: %s", self.params)

    def get(self):
        """
        Executes a GET request from the specified API.

        User's api_key is sent in request parameters.

        Returns:
            A requests.Response object with the result of the HTTP call.
        """
        self.params["api_key"] = self.api_key
        logger.info(
            "Calling %s with params: %s",
            self.url,
            json.dumps(self.params, indent=2),
        )
        return requests.get(
            self.url, params=self.params, headers=self.headers, timeout=None
        )

    def post(self):
        """
        Executes a POST request to the specified API.

        User's api_key is sent as a 'X-api-key' header.

        Returns:
            A requests.Response object with the result of the HTTP call.
        """
        self.headers["X-api-key"] = self.api_key
        logger.info(
            "Calling %s with params: %s",
            self.url,
            json.dumps(self.params, indent=2),
        )
        return requests.post(
            self.url, json=self.params, headers=self.headers, timeout=None
        )
