"""
A settings singleton to share settings across different modules of the package.
"""

from pydantic.dataclasses import dataclass


@dataclass
class Settings:
    """
    Singleton holding app's settings.
    """

    api_key: str = None
    base_path: str = "https://api.peopledatalabs.com/"
    log_level: str = None
    log_format: str = "{asctime} [{levelname}] - {name}.{funcName}: {message}"
    version: str = "v5"
    version_re: str = r"^v[0-9]$"
    sandbox_base_path: str = "https://sandbox.api.peopledatalabs.com/"
    sdk_version: str = "7.0.0"


settings = Settings()
