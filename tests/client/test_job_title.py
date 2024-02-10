"""
Tests calls to the job_title API.
"""

import logging
import pytest

import requests

from peopledatalabs.errors import EmptyParametersException


logging.basicConfig()
logger = logging.getLogger("PeopleDataLabs.tests.job_title")


@pytest.mark.usefixtures("client_with_fake_api_key")
def test_job_title_no_params_throw_error(client_with_fake_api_key):
    """
    Tests calling the job_title method without parameters.

    Should raise EmptyParametersException
    """
    with pytest.raises(EmptyParametersException):
        client_with_fake_api_key.job_title()


@pytest.mark.usefixtures("client")
def test_api_endpoint_job_title(client):
    """
    Tests successful execution of job_title API.
    """
    completion = client.job_title(
        job_title="data scientist",
    )
    assert isinstance(completion, requests.Response)
    assert completion.status_code == 200
