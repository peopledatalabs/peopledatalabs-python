from pydantic import (
    SecretStr
)


def json_defaults(value):
    mapping = {
        SecretStr: str
    }
    return mapping[type(value)](value)
