"""
All tests related to the Person object of the client instance"
"""


import logging
import pytest

import requests

from peopledatalabs_python.errors import EmptyParametersException
from peopledatalabs_python.main import Person


logging.basicConfig()
logger = logging.getLogger("PeopleDataLabs.tests")


@pytest.mark.usefixtures("client_with_fake_api_key")
def test_init_person(client_with_fake_api_key):
    """
    Tests init of Person object as attribute of client object.
    """
    assert isinstance(client_with_fake_api_key.person, Person)


@pytest.mark.usefixtures("client_with_fake_api_key")
def test_enrichment_no_params_throw_error(client_with_fake_api_key):
    """
    Tests calling the enrichment method without parameters.
    Should raise EmptyParametersException
    """
    with pytest.raises(EmptyParametersException):
        client_with_fake_api_key.person.enrichment()


@pytest.mark.usefixtures("client")
def test_api_endpoint_enrichment(client):
    """
    Tests successful execution of enrichment API.
    """
    enriched = client.person.enrichment(
        profile="https://www.linkedin.com/in/guido-van-rossum-4a0756/"
    )
    assert isinstance(enriched, requests.Response)
    assert enriched.status_code == 200


@pytest.mark.usefixtures("client")
def test_api_endpoint_enrichment_list_values(client):
    """
    Tests successful execution of enrichment API.
    Parameters with list values.
    """
    enriched = client.person.enrichment(
        name=["Sean Thorne"],
        profile=["www.twitter.com/seanthorne5", "linkedin.com/in/seanthorne"]
    )
    assert isinstance(enriched, requests.Response)
    assert enriched.status_code == 200
