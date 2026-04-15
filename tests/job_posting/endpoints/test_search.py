"""
Tests calls to the job_posting/search API.
"""

import base64
import json
import logging

import pytest
from pydantic.v1 import ValidationError
import requests

from peopledatalabs.errors import EmptyParametersException
from peopledatalabs.models.job_posting import (
    JobPostingParamSearchModel,
    JobPostingQuerySearchModel,
)


logging.basicConfig()
logger = logging.getLogger("PeopleDataLabs.tests.job_posting.search")


@pytest.mark.usefixtures("client_with_fake_api_key")
def test_search_empty_params_throw_error(client_with_fake_api_key):
    """
    Tests calling the search method without parameters.

    Should raise EmptyParametersException.
    """
    with pytest.raises(EmptyParametersException):
        client_with_fake_api_key.job_posting.search()


def test_param_model_size_out_of_range_raises_validation_error():
    """
    Param-mode size must be between 1 and 100.
    """
    with pytest.raises(ValidationError):
        JobPostingParamSearchModel(title="engineer", size=0)
    with pytest.raises(ValidationError):
        JobPostingParamSearchModel(title="engineer", size=101)


def test_param_model_invalid_remote_work_policy_raises_validation_error():
    """
    remote_work_policy must be one of the enum values.
    """
    with pytest.raises(ValidationError):
        JobPostingParamSearchModel(remote_work_policy="hybrid")


def test_param_model_invalid_salary_period_raises_validation_error():
    """
    salary_period must be one of the enum values.
    """
    with pytest.raises(ValidationError):
        JobPostingParamSearchModel(salary_period="fortnight")


def test_query_model_scroll_token_accepts_base64_string():
    """
    scroll_token may be passed as a base64-url-encoded JSON string and is
    decoded into a list.
    """
    raw = [1, 2, 3]
    encoded = base64.urlsafe_b64encode(
        json.dumps(raw).encode()
    ).decode()
    model = JobPostingQuerySearchModel(query={"match_all": {}}, scroll_token=encoded)
    assert model.scroll_token == raw


def test_query_model_scroll_token_accepts_list_passthrough():
    """
    scroll_token already in list form passes through unchanged.
    """
    model = JobPostingQuerySearchModel(
        query={"match_all": {}}, scroll_token=[1, 2, 3]
    )
    assert model.scroll_token == [1, 2, 3]


@pytest.mark.usefixtures("client")
def test_api_endpoint_search_query(client):
    """
    Tests successful execution of search API by ES query.
    """
    es_query = {
        "query": {
            "bool": {
                "must": [
                    {"term": {"title_role": "engineering"}},
                ]
            }
        }
    }
    data = {
        "query": es_query,
        "size": 10,
        "pretty": True,
    }
    response = client.job_posting.search(**data)
    assert isinstance(response, requests.Response)
    assert response.status_code == 200


@pytest.mark.usefixtures("client")
def test_api_endpoint_search_params(client):
    """
    Tests successful execution of search API by field parameters.
    """
    data = {
        "title_role": "engineering",
        "remote_work_policy": "remote",
        "size": 10,
        "pretty": True,
    }
    response = client.job_posting.search(**data)
    assert isinstance(response, requests.Response)
    assert response.status_code == 200
