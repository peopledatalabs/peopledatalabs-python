import logging

import pytest
from pydantic import ValidationError

from peopledatalabs_python import __version__
from peopledatalabs_python.main import PDLPY


logging.basicConfig()
logger = logging.getLogger("PeopleDataLabs.tests")


def test_version():
    assert __version__ == '0.1.0'


@pytest.mark.usefixtures("fake_api_key")
def test_init_defaults(fake_api_key):
    client = PDLPY(fake_api_key)
    assert client.base_path == "https://api.peopledatalabs.com/v5"


@pytest.mark.usefixtures("fake_api_key")
def test_init_defaults_base_path_only(fake_api_key):
    client = PDLPY(
        api_key=fake_api_key,
        base_path="https://google.com",
    )
    assert client.base_path == "https://google.com"


@pytest.mark.usefixtures("fake_api_key")
def test_init_defaults_version_only(fake_api_key):
    client = PDLPY(
        api_key=fake_api_key,
        version="v4"
    )
    assert client.base_path == "https://api.peopledatalabs.com/v4"


def test_init_no_api_key_raises_validation_error():
    with pytest.raises(ValidationError):
        PDLPY()


def test_init_invalid_api_key_raises_validation_error():
    with pytest.raises(ValidationError):
        PDLPY(api_key=[])


@pytest.mark.usefixtures("fake_api_key")
def test_init_invalid_base_path_raises_validation_error(fake_api_key):
    with pytest.raises(ValidationError):
        PDLPY(
            api_key="123",
            base_path="foo",
        )


@pytest.mark.usefixtures("fake_api_key")
def test_init_invalid_version_rasies_validation_error(fake_api_key):
    with pytest.raises(ValidationError):
        PDLPY(
            api_key="123",
            version="5v"
        )
