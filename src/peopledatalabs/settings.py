"""
A settings singleton to share settings across different modules of the package.

Settings also loads environment variables eventually declared in an .env
file.
"""

import os

from dotenv import find_dotenv, load_dotenv
from pydantic import HttpUrl, SecretStr
from pydantic.dataclasses import dataclass


@dataclass
class Settings:
    """
    Singleton holding app's settings.

    Settings are eventually overridden if a .env file is provided, or
    environment variables are defined.
    """

    api_key: SecretStr = None
    base_path: HttpUrl = "https://api.peopledatalabs.com/"
    log_level: str = None
    log_format: str = "{asctime} [{levelname}] - {name}.{funcName}: {message}"
    version: str = "v5"
    version_re: str = r"^v[0-9]$"

    def __post_init__(self):
        load_dotenv(dotenv_path=find_dotenv(usecwd=True))
        for key in self.__dict__:
            if key == "api_key":
                self.api_key = os.getenv("PDL_API_KEY", self.api_key)
            else:
                self.__dict__[key] = os.getenv(key.upper(), self.__dict__[key])


settings = Settings()
