"""
Tests calls to the sandbox person/enrich API.
"""


import logging
import pytest

import requests

from peopledatalabs.errors import EmptyParametersException


logging.basicConfig()
logger = logging.getLogger("PeopleDataLabs.tests.sandbox.person.enrichment")


@pytest.mark.usefixtures("client_with_fake_api_key")
def test_enrichment_sandbox_no_params_throw_error(client_with_fake_api_key):
    """
    Tests calling the sandbox person enrichment method without parameters.

    Should raise EmptyParametersException
    """
    with pytest.raises(EmptyParametersException):
        client_with_fake_api_key.person.enrichment()


@pytest.mark.usefixtures("client_sandbox_enabled")
def test_api_endpoint_sandbox_enrichment(client_sandbox_enabled):
    """
    Tests successful execution of enrichment API.
    """
    enriched = client_sandbox_enabled.person.enrichment(
        email="irussell@example.org"
    )
    assert isinstance(enriched, requests.Response)
    assert enriched.status_code == 200
