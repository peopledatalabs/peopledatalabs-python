"""
Tests calls to the person/identify API.
"""


import logging
import pytest

from pydantic import ValidationError
import requests

from peopledatalabs_python.errors import EmptyParametersException


logging.basicConfig()
logger = logging.getLogger("PeopleDataLabs.tests.person.identify")


@pytest.mark.usefixtures("client_with_fake_api_key")
def test_identify_empty_params_throw_error(client_with_fake_api_key):
    """
    Tests calling the identify method without parameters.

    Should raise EmptyParametersException
    """
    with pytest.raises(EmptyParametersException):
        client_with_fake_api_key.person.identify()


@pytest.mark.usefixtures("client")
def test_api_endpoint_identify(client):
    """
    Tests successful execution of identify API.
    """
    identified = client.person.identify(
        name="sean thorne"
    )
    assert isinstance(identified, requests.Response)
    assert identified.status_code == 200
    assert "matches" in identified.json()


@pytest.mark.usefixtures("client")
def test_api_endpoint_identify_list_values_raise_validation_error(client):
    """
    Raises ValidationError for parameters passed as lists to the identify API.
    """
    with pytest.raises(ValidationError):
        client.person.identify(
            name=["Sean Thorne"],
            profile=[
                "www.twitter.com/seanthorne5",
                "linkedin.com/in/seanthorne"
            ]
        )
