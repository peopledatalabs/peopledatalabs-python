"""
Tests calls to the person/bulk API.
"""


import logging
import pytest

from pydantic.v1 import ValidationError
import requests

from peopledatalabs.errors import EmptyParametersException


logging.basicConfig()
logger = logging.getLogger("PeopleDataLabs.tests.company.bulk")


@pytest.mark.usefixtures("client_with_fake_api_key")
def test_bulk_empty_params_throw_error(client_with_fake_api_key):
    """
    Tests calling the bulk method without parameters.

    Should raise EmptyParametersException
    """
    with pytest.raises(EmptyParametersException):
        client_with_fake_api_key.company.bulk()


@pytest.mark.usefixtures("client")
def test_api_endpoint_bulk_empty_requests_raise_validation_error(client):
    """
    Tests successful execution of company bulk enrichment API.
    """
    data = {"requests": []}
    with pytest.raises(ValidationError):
        client.company.bulk(**data)


@pytest.mark.usefixtures("client")
def test_api_endpoint_bulk_requests_no_params_raise_validation_error(client):
    """
    Tests successful execution of company bulk enrichment API.
    """
    data = {"requests": [{"metadata": {"company_id": "123"}, "params": {}}]}
    with pytest.raises(ValidationError):
        client.company.bulk(**data)


@pytest.mark.usefixtures("client")
def test_api_endpoint_bulk(client):
    """
    Tests successful execution of company bulk enrichment API.
    """
    data = {
        "requests": [
            {"params": {"profile": "linkedin.com/company/peopledatalabs"}},
            {"params": {"profile": "linkedin.com/company/apple"}},
        ]
    }
    response = client.company.bulk(**data)
    assert isinstance(response, requests.Response)
    assert response.status_code == 200


@pytest.mark.usefixtures("client")
def test_api_endpoint_bulk_with_metadata(client):
    """
    Tests successful execution of company bulk enrichment API.
    """
    data = {
        "requests": [
            {
                "metadata": {"company_id": "123"},
                "params": {
                    "profile": "linkedin.com/company/peopledatalabs",
                },
            },
            {
                "metadata": {"company_id": "345"},
                "params": {
                    "profile": "https://www.linkedin.com/company/apple/",
                },
            },
        ]
    }
    response = client.company.bulk(**data)
    assert isinstance(response, requests.Response)
    assert response.status_code == 200
