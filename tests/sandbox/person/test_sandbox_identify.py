"""
Tests calls to the sandbox person/identify API.
"""


import logging
import pytest

from pydantic import ValidationError
import requests

from peopledatalabs.errors import EmptyParametersException


logging.basicConfig()
logger = logging.getLogger("PeopleDataLabs.tests.sandbox.person.identify")


@pytest.mark.usefixtures("client_with_fake_api_key")
def test_identify_sandbox__empty_params_throw_error(client_with_fake_api_key):
    """
    Tests calling the identify method without parameters.

    Should raise EmptyParametersException
    """
    with pytest.raises(EmptyParametersException):
        client_with_fake_api_key.person.identify()


@pytest.mark.usefixtures("client_sandbox_enabled")
def test_api_endpoint_sandbox_identify(client_sandbox_enabled):
    """
    Tests successful execution of identify API.
    """
    identified = client_sandbox_enabled.person.identify(company="walmart")
    assert isinstance(identified, requests.Response)
    assert identified.status_code == 200
    assert "matches" in identified.json()


@pytest.mark.usefixtures("client_sandbox_enabled")
def test_api_endpoint_sandbox_identify_list_values_raise_validation_error(
    client_sandbox_enabled,
):
    """
    Raises ValidationError for parameters passed as lists to the identify API.
    """
    with pytest.raises(ValidationError):
        client_sandbox_enabled.person.identify(
            company=["walmart"],
        )
