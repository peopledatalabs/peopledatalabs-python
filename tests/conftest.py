"""
Pytest testing configuration file.
"""


import uuid

import pytest

from peopledatalabs.main import PDLPY
from peopledatalabs.logger import get_logger


logger = get_logger("tests")


@pytest.fixture(name="fake_api_key")
def fixture_fake_api_key():
    """
    Fixture which returns a randomly generated uuid4 as a fake API key.
    """
    return str(uuid.uuid4())


@pytest.fixture
def client():
    """
    Client instance loads API_KEY from .env file.
    """
    return PDLPY()


@pytest.fixture
def client_with_fake_api_key(fake_api_key):
    """
    Client instance with fake API key.
    """
    return PDLPY(api_key=fake_api_key)
