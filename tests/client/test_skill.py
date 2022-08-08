"""
Tests calls to the skill API.
"""


import logging
import pytest

from pydantic import ValidationError
import requests

from peopledatalabs.errors import EmptyParametersException


logging.basicConfig()
logger = logging.getLogger("PeopleDataLabs.tests.skill")


@pytest.mark.usefixtures("client_with_fake_api_key")
def test_skill_no_params_throw_error(client_with_fake_api_key):
    """
    Tests calling the skill method without parameters.

    Should raise EmptyParametersException
    """
    with pytest.raises(EmptyParametersException):
        client_with_fake_api_key.skill()


@pytest.mark.usefixtures("client")
def test_api_endpoint_skill(client):
    """
    Tests successful execution of skill API.
    """
    completion = client.skill(
        skill="c++",
    )
    assert isinstance(completion, requests.Response)
    assert completion.status_code == 200
