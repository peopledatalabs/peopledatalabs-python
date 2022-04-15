"""
Tests calls to the person/bulk API.
"""


import logging
import pytest

from pydantic import ValidationError
import requests

from peopledatalabs_python.errors import EmptyParametersException


logging.basicConfig()
logger = logging.getLogger("PeopleDataLabs.tests.person.bulk")


@pytest.mark.usefixtures("client_with_fake_api_key")
def test_bulk_empty_params_throw_error(client_with_fake_api_key):
    """
    Tests calling the bulk method without parameters.
    Should raise EmptyParametersException
    """
    with pytest.raises(EmptyParametersException):
        client_with_fake_api_key.person.bulk()


@pytest.mark.usefixtures("client")
def test_api_endpoint_bulk_empty_requests_raise_validation_error(client):
    """
    Tests successful execution of bulk API.
    """
    data = {
       "requests": []
    }
    with pytest.raises(ValidationError):
        client.person.bulk(**data)


@pytest.mark.usefixtures("client")
def test_api_endpoint_bulk_requests_no_params_raise_validation_error(client):
    """
    Tests successful execution of bulk API.
    """
    data = {
       "requests": [
            {
                "metadata": {
                    "user_id": "123"
                },
                "params": {}
            }
       ]
    }
    with pytest.raises(ValidationError):
        client.person.bulk(**data)


@pytest.mark.usefixtures("client")
def test_api_endpoint_bulk(client):
    """
    Tests successful execution of bulk API.
    """
    data = {
        "requests": [
            {
                "params": {
                    "profile": ["linkedin.com/in/seanthorne"]
                }
            },
            {
                "params": {
                    "profile": ["linkedin.com/in/randrewn"]
                }
            }
        ]
    }
    response = client.person.bulk(**data)
    assert isinstance(response, requests.Response)
    assert response.status_code == 200


@pytest.mark.usefixtures("client")
def test_api_endpoint_bulk_with_metadata(client):
    """
    Tests successful execution of bulk API.
    """
    data = {
        "requests": [
            {
                "metadata": {
                    "user_id": "123"
                },
                "params": {
                    "profile": ["linkedin.com/in/seanthorne"],
                    "location": ["SF Bay Area"],
                    "name": ["Sean F. Thorne"]
                }
            },
            {
                "metadata": {
                    "user_id": "345"
                },
                "params": {
                    "profile": ["https://www.linkedin.com/in/haydenconrad/"],
                    "first_name": "Hayden",
                    "last_name": "Conrad"
                }
            }
        ]
    }
    response = client.person.bulk(**data)
    assert isinstance(response, requests.Response)
    assert response.status_code == 200


@pytest.mark.usefixtures("client")
def test_api_endpoint_bulk_with_filtering(client):
    """
    Tests successful execution of bulk API.
    """
    data = {
        "required": "emails AND profiles",
        "requests": [
            {
                "params": {
                    "profile": ["linkedin.com/in/seanthorne"],
                    "location": ["SF Bay Area"],
                    "name": ["Sean F. Thorne"]
                }
            },
            {
                "params": {
                    "profile": ["https://www.linkedin.com/in/haydenconrad/"],
                    "first_name": "Hayden",
                    "last_name": "Conrad"
                }
            }
        ]
    }
    response = client.person.bulk(**data)
    assert isinstance(response, requests.Response)
    assert len(response.json()) == 2
    assert response.status_code == 200
