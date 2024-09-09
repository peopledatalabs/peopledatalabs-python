"""
Tests calls to the ip API.
"""

import logging
import pytest

import requests

from peopledatalabs.errors import EmptyParametersException


logging.basicConfig()
logger = logging.getLogger("PeopleDataLabs.tests.ip")


@pytest.mark.usefixtures("client_with_fake_api_key")
def test_ip_no_params_throw_error(client_with_fake_api_key):
    """
    Tests calling the ip method without parameters.

    Should raise EmptyParametersException
    """
    with pytest.raises(EmptyParametersException):
        client_with_fake_api_key.ip()


@pytest.mark.usefixtures("client")
def test_api_endpoint_ip(client):
    """
    Tests successful execution of ip API.
    """
    completion = client.ip(
        ip="72.212.42.169",
    )
    assert isinstance(completion, requests.Response)
    assert completion.status_code == 200


@pytest.mark.usefixtures("client")
def test_api_endpoint_ip(client):
    """
    Tests successful execution of ip API with min_confidence.
    """
    completion = client.ip(
        ip="72.212.42.169",
        min_confidence="very high",
    )
    assert isinstance(completion, requests.Response)
    assert completion.status_code == 200
