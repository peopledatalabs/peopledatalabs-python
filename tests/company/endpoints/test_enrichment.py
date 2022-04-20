"""
Tests calls to the company/enrich API.
"""


import logging
import pytest

from pydantic import ValidationError
import requests

from peopledatalabs_python.errors import EmptyParametersException


logging.basicConfig()
logger = logging.getLogger("PeopleDataLabs.tests.company.enrichment")


@pytest.mark.usefixtures("client_with_fake_api_key")
def test_enrichment_no_params_throw_error(client_with_fake_api_key):
    """
    Tests calling the enrichment method without parameters.

    Should raise EmptyParametersException
    """
    with pytest.raises(EmptyParametersException):
        client_with_fake_api_key.company.enrichment()


@pytest.mark.usefixtures("client")
def test_api_endpoint_enrichment(client):
    """
    Tests successful execution of enrichment API.
    """
    enriched = client.company.enrichment(
        name="google", website="google.com", min_likelihood=5, required="size"
    )
    assert isinstance(enriched, requests.Response)
    assert enriched.status_code == 200


@pytest.mark.usefixtures("client")
def test_api_endpoint_enrichment_ambiguous_raises_validation_error(client):
    """
    Tests successful execution of enrichment API.
    """
    with pytest.raises(ValidationError):
        client.company.enrichment(
            region="california", min_likelihood=5, required="size"
        )
