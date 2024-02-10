"""
Tests calls to the company/clean API.
"""

import logging
import pytest

import requests

from peopledatalabs.errors import EmptyParametersException


logging.basicConfig()
logger = logging.getLogger("PeopleDataLabs.tests.company.cleaner")


@pytest.mark.usefixtures("client_with_fake_api_key")
def test_cleaner_no_params_throw_error(client_with_fake_api_key):
    """
    Tests calling the cleaner method without parameters.

    Should raise EmptyParametersException
    """
    with pytest.raises(EmptyParametersException):
        client_with_fake_api_key.company.cleaner()


@pytest.mark.usefixtures("client")
def test_api_endpoint_cleaner(client):
    """
    Tests successful execution of cleaner API.
    """
    cleaned = client.company.cleaner(
        website="peopledatalabs.com",
    )
    assert isinstance(cleaned, requests.Response)
    assert cleaned.status_code == 200
