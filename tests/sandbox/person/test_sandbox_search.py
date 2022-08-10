"""
Tests calls to the sandbox person/search API.
"""


import logging
import pytest

from pydantic import ValidationError
import requests

from peopledatalabs.errors import EmptyParametersException


logging.basicConfig()
logger = logging.getLogger("PeopleDataLabs.tests.sandbox.person.search")


@pytest.mark.usefixtures("client_with_fake_api_key")
def test_search_sandbox_empty_params_throw_error(client_with_fake_api_key):
    """
    Tests calling the search method without parameters.

    Should raise EmptyParametersException
    """
    with pytest.raises(EmptyParametersException):
        client_with_fake_api_key.person.search()


@pytest.mark.usefixtures("client_sandbox_enabled")
def test_api_endpoint_sandbox_search_query(client_sandbox_enabled):
    """
    Tests successful execution of search API by ES query.
    """
    es_query = {
        "query": {
            "bool": {
                "must": [
                    {"term": {"location_country": "mexico"}},
                ]
            }
        }
    }
    data = {
        "query": es_query,
        "size": 10,
        "pretty": True,
    }
    response = client_sandbox_enabled.person.search(**data)
    assert isinstance(response, requests.Response)
    assert response.status_code == 200


@pytest.mark.usefixtures("client_sandbox_enabled")
def test_api_endpoint_sandbox_search_sql(client_sandbox_enabled):
    """
    Tests successful execution of search API by SQL query.
    """
    sql_query = "SELECT * FROM person WHERE location_country='mexico';"
    data = {
        "sql": sql_query,
        "size": 10,
        "pretty": True,
    }
    response = client_sandbox_enabled.person.search(**data)
    assert isinstance(response, requests.Response)
    assert response.status_code == 200


@pytest.mark.usefixtures("client_sandbox_enabled")
def test_api_endpoint_sandbox_search_both_queries_raises_validation_error(
    client_sandbox_enabled,
):
    """
    Raises ValidationError if both ES and SQL queries are used.
    """
    es_query = {
        "query": {
            "bool": {
                "must": [
                    {"term": {"location_country": "mexico"}},
                ]
            }
        }
    }
    sql_query = "SELECT * FROM person WHERE location_country='mexico';"
    data = {
        "query": es_query,
        "sql": sql_query,
        "size": 10,
        "pretty": True,
    }
    with pytest.raises(ValidationError):
        client_sandbox_enabled.person.search(**data)


@pytest.mark.usefixtures("client")
def test_api_endpoint_sandbox_search_invalid_dataset_raises_validation_error(
    client_sandbox_enabled,
):
    """
    Raises ValidationError with invalid dataset.
    """
    es_query = {
        "query": {
            "bool": {
                "must": [
                    {"term": {"location_country": "mexico"}},
                ]
            }
        }
    }
    data = {
        "query": es_query,
        "size": 10,
        "pretty": True,
        "dataset": "invalid",
    }
    with pytest.raises(ValidationError):
        client_sandbox_enabled.person.search(**data)
