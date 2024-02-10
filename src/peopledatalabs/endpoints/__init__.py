"""
Package to resolve endpoints from the People Data Labs' API.
"""

from typing import Type

from pydantic.v1 import (
    BaseModel,
    HttpUrl,
    StrictStr,
)
from pydantic.v1.dataclasses import dataclass

from ..errors import InvalidEndpointError
from ..requests import Request
from ..utils import check_empty_parameters

headers = {
    "Accept-Encoding": "gzip",
    "User-Agent": "PDL-PYTHON-SDK",
    "Content-Type": "application/json",
}


@dataclass
class Endpoint:
    """
    Base class for all endpoints.

    Args:
        api_key (str): The authentication API key for API calls.
        base_path (str): PeopleDataLabs' API base URL.
        section: (:obj:`str`, optional): The section to prepend to the
            API endpoint.
    """

    api_key: str
    base_path: HttpUrl
    section: str = None

    def get_url(self, endpoint: str):
        """
        Forms the URL for the API call.

        Args:
            endpoint (str): The endpoint of the API to call.
        """
        url = self.base_path
        if self.section:
            url += "/" + self.section
        url += "/" + endpoint

        return url

    def __getattr__(self, method_name):
        """
        Raises InvalidEndpointError when an undefined method is called.
        """

        # disregard dunder methods
        if method_name.startswith("__") and method_name.endswith("__"):
            return self.__getattribute__(method_name)

        # pylint: disable=unused-argument
        def method(*args, **kwargs):
            cls_name = self.__class__.__name__
            raise InvalidEndpointError(
                f"Invalid method {method_name} called for section {cls_name}."
            )

        return method

    @check_empty_parameters
    def _bulk(self, model: Type[BaseModel], **kwargs):
        """
        Calls PeopleDataLabs' bulk enrichment API.

        Args:
            model: The model used for parameters validation.
            **kwargs: Parameters for the API as defined
                in the documentation.

        Returns:
            A requests.Response object with the result of the HTTP call.
        """
        url = self.get_url(endpoint="bulk")
        return Request(
            api_key=self.api_key,
            url=url,
            headers=headers,
            params=kwargs,
            validator=model,
        ).post()

    @check_empty_parameters
    def _cleaner(self, model: Type[BaseModel], **kwargs):
        """
        Calls PeopleDataLabs' cleaner API.

        Args:
            model: The model used for parameters validation.
            **kwargs: Parameters for the API as defined
                in the documentation.

        Returns:
            A requests.Response object with the result of the HTTP call.
        """
        url = self.get_url(endpoint="clean")
        return Request(
            api_key=self.api_key,
            url=url,
            headers=headers,
            params=kwargs,
            validator=model,
        ).get()

    @check_empty_parameters
    def _enrichment(self, model: Type[BaseModel], **kwargs):
        """
        Calls PeopleDataLabs' enrichment API.

        Args:
            model: The model used for parameters validation.
            **kwargs: Parameters for the API as defined
                in the documentation.

        Returns:
            A requests.Response object with the result of the HTTP call.
        """
        url = self.get_url(endpoint="enrich")
        return Request(
            api_key=self.api_key,
            url=url,
            headers=headers,
            params=kwargs,
            validator=model,
        ).get()

    @check_empty_parameters
    def _identify(self, model: Type[BaseModel], **kwargs):
        """
        Calls PeopleDataLabs' identify API.

        Args:
            model: The model used for parameters validation.
            **kwargs: Parameters for the API as defined
                in the documentation.

        Returns:
            A requests.Response object with the result of the HTTP call.
        """
        url = self.get_url(endpoint="identify")
        return Request(
            api_key=self.api_key,
            url=url,
            headers=headers,
            params=kwargs,
            validator=model,
        ).get()

    def _retrieve(
        self,
        model: Type[BaseModel],
        person_id: StrictStr,
        **kwargs,
    ):
        """
        Calls PeopleDataLabs' retrieve API.

        Args:
            model: The model used for parameters validation.
            person_id (str): The person's ID from the
                People Data Labs dataset;
            **kwargs: Additional parameters for the API as defined
                in the documentation.

        Returns:
            A requests.Response object with the result of the HTTP call.
        """
        url = self.get_url(endpoint="retrieve")
        url += "/" + person_id
        return Request(
            api_key=self.api_key,
            url=url,
            headers=headers,
            params=kwargs,
            validator=model,
        ).get()

    @check_empty_parameters
    def _search(self, model: Type[BaseModel], **kwargs):
        """
        Calls PeopleDataLabs' search API.

        Args:
            model: The model used for parameters validation.
            **kwargs: Parameters for the API as defined
                in the documentation.

        Returns:
            A requests.Response object with the result of the HTTP call.
        """
        url = self.get_url(endpoint="search")
        return Request(
            api_key=self.api_key,
            url=url,
            headers=headers,
            params=kwargs,
            validator=model,
        ).post()

    @check_empty_parameters
    def _company_bulk(self, model: Type[BaseModel], **kwargs):
        """
        Calls PeopleDataLabs' company bulk enrichment API.

        Args:
            model: The model used for parameters validation.
            **kwargs: Parameters for the API as defined
                in the documentation.

        Returns:
            A requests.Response object with the result of the HTTP call.
        """
        url = self.get_url(endpoint="enrich/bulk")
        return Request(
            api_key=self.api_key,
            url=url,
            headers=headers,
            params=kwargs,
            validator=model,
        ).post()
