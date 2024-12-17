"""
Tests calls to the autocomplete API.
"""

import logging
import pytest

from pydantic.v1 import ValidationError
import requests

from peopledatalabs.errors import EmptyParametersException


logging.basicConfig()
logger = logging.getLogger("PeopleDataLabs.tests.autocomplete")


@pytest.mark.usefixtures("client_with_fake_api_key")
def test_autocomplete_no_params_throw_error(client_with_fake_api_key):
    """
    Tests calling the autocomplete method without parameters.

    Should raise EmptyParametersException
    """
    with pytest.raises(EmptyParametersException):
        client_with_fake_api_key.autocomplete()


@pytest.mark.usefixtures("client_with_fake_api_key")
def test_api_endpoint_autocomplete_no_field_raises_validation_error(
    client_with_fake_api_key,
):
    """
    Tests validation of 'field' parameter.

    Should raise ValidationError
    """
    with pytest.raises(ValidationError):
        client_with_fake_api_key.autocomplete(
            text="data",
            size=10,
        )


@pytest.mark.usefixtures("client")
def test_api_endpoint_autocomplete(client):
    """
    Tests successful execution of autocomplete API.
    """
    completion = client.autocomplete(
        field="title",
        text="data",
        size=20,
    )
    assert isinstance(completion, requests.Response)
    assert completion.status_code == 200


@pytest.mark.usefixtures("client")
def test_api_endpoint_autocomplete_with_class(client):
    """
    Tests successful execution of autocomplete API with class field.
    """
    completion = client.autocomplete(
        field="class",
        text="sales",
        size=20,
        updated_title_roles=True,
    )
    assert isinstance(completion, requests.Response)
    assert completion.status_code == 200