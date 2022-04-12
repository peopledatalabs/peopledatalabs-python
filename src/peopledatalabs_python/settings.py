from dataclasses import dataclass
import json
import os

from dotenv import load_dotenv
from pydantic import (
    HttpUrl,
    SecretStr
)


@dataclass
class Settings():
    api_key: SecretStr = None
    base_path: HttpUrl = "https://api.peopledatalabs.com/"
    log_level: str = None
    log_format: str = "{asctime} [{levelname}] - {name}.{funcName}: {message}"
    version_re: str = r"^v[0-9]$"

    def __post_init__(self):
        load_dotenv()
        for key in self.__dict__:
            self.__dict__[key] = os.getenv(key.upper(), self.__dict__[key])

    def __repr__(self):
        return json.dumps(self.__dict__, indent=2)


settings = Settings()
