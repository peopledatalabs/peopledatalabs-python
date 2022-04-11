import logging
import pytest
import uuid

from pydantic import ValidationError

from peopledatalabs_python import __version__
from peopledatalabs_python.defaults import Defaults
from peopledatalabs_python.main import PDLPY


logging.basicConfig()
logger = logging.getLogger("PeopleDataLabs.tests")


def test_version():
    assert __version__ == '0.1.0'


def test_init_defaults():
    client = PDLPY(str(uuid.uuid4()))
    assert client.base_path == Defaults.base_path


def test_init_params():
    base_path = "https://api.peopledatalabs.com/"
    version = "v5"
    client = PDLPY(str(uuid.uuid4()), base_path, version)
    assert client.base_path == (base_path + version)


def test_init_invalid_api_key_raises_validation_error():
    with pytest.raises(ValidationError):
        PDLPY(api_key=[])


def test_init_invalid_base_path_raises_validation_error():
    with pytest.raises(ValidationError):
        PDLPY(
            api_key="123",
            base_path="foo",
        )


def test_init_invalid_version_rasies_validation_error():
    with pytest.raises(ValidationError):
        PDLPY(
            api_key="123",
            version="5v"
        )
