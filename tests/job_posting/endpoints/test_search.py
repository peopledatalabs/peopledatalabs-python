"""
Tests calls to the job_posting/search API.
"""

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


def test_query_model_size_out_of_range_raises_validation_error():
    """
    Query-mode size must also be between 1 and 100.
    """
    with pytest.raises(ValidationError):
        JobPostingQuerySearchModel(query={"match_all": {}}, size=0)
    with pytest.raises(ValidationError):
        JobPostingQuerySearchModel(query={"match_all": {}}, size=101)


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


def test_param_model_is_active_omitted_by_default():
    """
    is_active is an opt-in filter and must not be sent unless the caller
    sets it explicitly.
    """
    model = JobPostingParamSearchModel(title="engineer")
    assert "is_active" not in model.dict(exclude_none=True)


def test_scroll_token_round_trips_as_opaque_string():
    """
    scroll_token is the opaque base64 token returned by the API and must
    be passed back unchanged on subsequent calls.
    """
    token = "eyJhIjogMX0="
    query_model = JobPostingQuerySearchModel(
        query={"match_all": {}}, scroll_token=token
    )
    assert query_model.scroll_token == token

    param_model = JobPostingParamSearchModel(
        title="engineer", scroll_token=token
    )
    assert param_model.scroll_token == token


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
