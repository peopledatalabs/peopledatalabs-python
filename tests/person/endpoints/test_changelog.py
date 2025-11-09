"""
Tests calls to the person/changelog API.
"""

import logging
import pytest

import requests

from peopledatalabs.errors import EmptyParametersException


logging.basicConfig()
logger = logging.getLogger("PeopleDataLabs.tests.person.changelog")


@pytest.mark.usefixtures("client_with_fake_api_key")
def test_changelog_no_params_throw_error(client_with_fake_api_key):
    """
    Tests calling the changelog method without parameters.

    Should raise EmptyParametersException
    """
    with pytest.raises(EmptyParametersException):
        client_with_fake_api_key.person.changelog()


@pytest.mark.usefixtures("client")
def test_api_endpoint_changelog(client):
    """
    Tests successful execution of changelog API.
    """
    changelog = client.person.changelog(
        current_version="32.0", origin_version="31.2", type="updated"
    )
    assert isinstance(changelog, requests.Response)
    assert changelog.status_code == 200
