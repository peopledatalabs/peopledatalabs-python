"""
Pytest testing configuration file.
"""

import uuid

import os

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
    Client instance loads with real API key.
    """
    return PDLPY(api_key=os.environ["PDL_API_KEY"])


@pytest.fixture
def client_with_fake_api_key(fake_api_key):
    """
    Client instance with fake API key.
    """
    return PDLPY(api_key=fake_api_key)


@pytest.fixture
def client_sandbox_enabled():
    """
    Client instance loads with real API key and Sandbox enabled.
    """
    return PDLPY(sandbox=True, api_key=os.environ["PDL_API_KEY"])


@pytest.fixture
def client_env_test():
    """
    Client instance loads correct env variables.
    """
    os.environ["VERSION"] = "PDL_TEST_FAIL"
    os.environ["PDL_VERSION"] = "v6"

    p_i = PDLPY(sandbox=True)

    del os.environ["VERSION"]
    del os.environ["PDL_VERSION"]

    return p_i.version == "v6"
