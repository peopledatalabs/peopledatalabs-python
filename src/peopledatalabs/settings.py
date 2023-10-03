"""
A settings singleton to share settings across different modules of the package.

Settings also loads environment variables eventually declared in an .env
file.
"""

import os

from dotenv import find_dotenv, load_dotenv
from pydantic.v1 import HttpUrl
from pydantic.v1.dataclasses import dataclass


@dataclass
class Settings:
    """
    Singleton holding app's settings.

    Settings are eventually overridden if a .env file is provided, or
    environment variables are defined.

    All env variables should be in the form of PDL_<setting name>
    """

    api_key: str = None
    base_path: HttpUrl = "https://api.peopledatalabs.com/"
    log_level: str = None
    log_format: str = "{asctime} [{levelname}] - {name}.{funcName}: {message}"
    version: str = "v5"
    version_re: str = r"^v[0-9]$"
    sandbox_base_path: HttpUrl = "https://sandbox.api.peopledatalabs.com/"

    def __post_init__(self):
        load_dotenv(dotenv_path=find_dotenv(usecwd=True))
        for key in self.__dict__:
            env_key = "PDL_" + key.upper()
            self.__dict__[key] = os.getenv(env_key, self.__dict__[key])


settings = Settings()
