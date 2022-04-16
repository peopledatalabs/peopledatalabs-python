"""
Package to resolve endpoints from the People Data Labs' API.
"""


from pydantic import (
    HttpUrl,
    SecretStr,
)
from pydantic.dataclasses import dataclass


@dataclass
class Endpoint:
    """
    Base class for all endpoints.

    Args:
        api_key (str): The authentication API key for API calls.
        base_path (str): PeopleDataLabs' API base URL.
    """

    api_key: SecretStr
    base_path: HttpUrl
    section: str = None

    def _get_url(self, endpoint: str):
        url = self.base_path
        if self.section:
            url += "/" + self.section
        url += "/" + endpoint

        return url
