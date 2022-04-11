from dataclasses import dataclass

from pydantic import HttpUrl


@dataclass
class Defaults():
    version: str = "v5"
    _base_path: str = "https://api.peopledatalabs.com/{}"

    def base_path(self) -> HttpUrl:
        return self._base_path + self.version
