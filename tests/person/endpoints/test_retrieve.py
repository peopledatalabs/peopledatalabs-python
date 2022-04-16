"""
Tests calls to the person/retrieve API.
"""


import logging
import pytest

from pydantic import ValidationError
import requests


logging.basicConfig()
logger = logging.getLogger("PeopleDataLabs.tests.person.retrieve")


@pytest.mark.usefixtures("client_with_fake_api_key")
def test_retrieve_empty_params_throw_error(client_with_fake_api_key):
    """
    Tests calling the retrieve method without parameters.
    Should raise ValidationError
    """
    with pytest.raises(ValidationError):
        client_with_fake_api_key.person.retrieve()


@pytest.mark.usefixtures("client")
def test_api_endpoint_retrieve_person_id_validation_error(client):
    """
    Tests successful execution of retrieve API.
    """
    with pytest.raises(ValidationError):
        client.person.retrieve(
            person_id=1
        )


@pytest.mark.usefixtures("client")
def test_api_endpoint_retrieve(client):
    """
    Tests successful execution of retrieve API.
    """
    retrieved = client.person.retrieve(
        person_id="qEnOZ5Oh0poWnQ1luFBfVw_0000"
    )
    assert isinstance(retrieved, requests.Response)
    assert retrieved.status_code == 200
