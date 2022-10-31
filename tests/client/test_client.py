"""
All tests related to the client instance.
"""


import logging

import pytest
from pydantic import ValidationError

from peopledatalabs import __version__
from peopledatalabs.main import PDLPY


logging.basicConfig()
logger = logging.getLogger("PeopleDataLabs.tests")


def test_version():
    """
    Version check.
    """
    assert __version__ == "1.1.2"


@pytest.mark.usefixtures("fake_api_key")
def test_init_defaults(fake_api_key):
    """
    Tests that a default init of the client, with api key only, will have
    `base_path` set correctly from default.
    """
    client = PDLPY(fake_api_key)
    assert client.base_path == "https://api.peopledatalabs.com/v5"


@pytest.mark.usefixtures("fake_api_key")
def test_init_defaults_base_path_only(fake_api_key):
    """
    Tests passing `base_path`.

    bclient.ase_path should be specified base_path
    """
    client = PDLPY(
        api_key=fake_api_key,
        base_path="https://google.com",
    )
    assert client.base_path == "https://google.com"


@pytest.mark.usefixtures("fake_api_key")
def test_init_defaults_version_only(fake_api_key):
    """
    Tests passing only version.

    `base_path` should have default base path and specified version.
    """
    client = PDLPY(api_key=fake_api_key, version="v4")
    assert client.base_path == "https://api.peopledatalabs.com/v4"


def test_init_no_api_key_raises_validation_error():
    """
    Tests that instantiating the client without providing either an .env file
    or an api key explicitly, a ValidationError is raised.

    To make this test pass either ".env" file should not exist or
    env_file modified in get_settings()
    """
    with pytest.raises(ValidationError):
        PDLPY()


def test_init_invalid_api_key_raises_validation_error():
    """
    Tests passing an invalid type for `api_key`.

    Should raise ValidationError.
    """
    with pytest.raises(ValidationError):
        PDLPY(api_key=[])


@pytest.mark.usefixtures("fake_api_key")
def test_init_invalid_base_path_raises_validation_error(fake_api_key):
    """
    Tests passing an invalid type for `base_path`.

    Should raise ValidationError.
    """
    with pytest.raises(ValidationError):
        PDLPY(
            api_key=fake_api_key,
            base_path="foo",
        )


@pytest.mark.usefixtures("fake_api_key")
def test_init_invalid_version_rasies_validation_error(fake_api_key):
    """
    Tests passing an invalid type for `version`.

    Should raise ValidationError.
    """
    with pytest.raises(ValidationError):
        PDLPY(api_key=fake_api_key, version="5v")
