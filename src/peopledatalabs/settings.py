"""
A settings singleton to share settings across different modules of the package.
"""

from pydantic.v1 import HttpUrl
from pydantic.v1.dataclasses import dataclass


@dataclass
class Settings:
    """
    Singleton holding app's settings.
    """

    api_key: str = None
    base_path: HttpUrl = "https://api.peopledatalabs.com/"
    log_level: str = None
    log_format: str = "{asctime} [{levelname}] - {name}.{funcName}: {message}"
    version: str = "v5"
    version_re: str = r"^v[0-9]$"
    sandbox_base_path: HttpUrl = "https://sandbox.api.peopledatalabs.com/"


settings = Settings()
