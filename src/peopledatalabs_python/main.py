"""
Client's main module.
"""


from pydantic import (
    HttpUrl,
    SecretStr,
    constr,
)
from pydantic.dataclasses import dataclass


from .endpoints.person import Person
from .logger import get_logger
from .settings import settings


logger = get_logger()


@dataclass
class PDLPY():
    """
    Client's main class.
    All methods derive from the instantiation of this class.

    Args:
        api_key: The authentication API key for API calls.
        base_path: PeopleDataLabs' API base URL, with version.
        version: PeopleDataLabs' API version to call. Will be used only if
            base_path has no value.
    """
    api_key: SecretStr = settings.api_key
    base_path: HttpUrl = None
    version: constr(regex=settings.version_re) = settings.version
    log_level: str = None

    def __post_init__(self):
        """
        Sets the actual base_path and sets log_level globally across modules.
        """
        if self.base_path is None:
            self.base_path = settings.base_path + self.version
        if self.log_level is not None:
            settings.log_level = self.log_level
            logger.setLevel(self.log_level)

        self.person = Person(self.api_key, self.base_path)
