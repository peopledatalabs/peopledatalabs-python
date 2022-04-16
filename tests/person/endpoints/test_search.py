"""
Tests calls to the person/search API.
"""


import logging
import pytest

from pydantic import ValidationError
import requests

from peopledatalabs_python.errors import EmptyParametersException


logging.basicConfig()
logger = logging.getLogger("PeopleDataLabs.tests.person.search")


@pytest.mark.usefixtures("client_with_fake_api_key")
def test_search_empty_params_throw_error(client_with_fake_api_key):
    """
    Tests calling the search method without parameters.

    Should raise EmptyParametersException
    """
    with pytest.raises(EmptyParametersException):
        client_with_fake_api_key.person.search()


@pytest.mark.usefixtures("client")
def test_api_endpoint_search_query(client):
    """
    Tests successful execution of search API by ES query.
    """
    es_query = {
        "query": {
            "bool": {
                "must": [
                    {"term": {"location_country": "mexico"}},
                    {"term": {"job_title_role": "health"}}
                ]
            }
        }
    }
    data = {
        "query": es_query,
        "size": 10,
        "pretty": True,
        "dataset": "phone, mobile_phone",
    }
    response = client.person.search(**data)
    assert isinstance(response, requests.Response)
    assert response.status_code == 200


@pytest.mark.usefixtures("client")
def test_api_endpoint_search_sql(client):
    """
    Tests successful execution of search API by SQL query.
    """
    sql_query = (
        "SELECT * FROM person"
        " WHERE location_country='mexico'"
        " AND job_title_role='health'"
        " AND phone_numbers IS NOT NULL;"
    )
    data = {
        "sql": sql_query,
        "size": 10,
        "pretty": True,
        "dataset": "phone, mobile_phone",
    }
    response = client.person.search(**data)
    assert isinstance(response, requests.Response)
    assert response.status_code == 200


@pytest.mark.usefixtures("client")
def test_api_endpoint_search_both_queries_raises_validation_error(client):
    """
    Raises ValidationError if both ES and SQL queries are used.
    """
    es_query = {
        "query": {
            "bool": {
                "must": [
                    {"term": {"location_country": "mexico"}},
                    {"term": {"job_title_role": "health"}}
                ]
            }
        }
    }
    sql_query = (
        "SELECT * FROM person"
        " WHERE location_country='mexico'"
        " AND job_title_role='health'"
        " AND phone_numbers IS NOT NULL;"
    )
    data = {
        "query": es_query,
        "sql": sql_query,
        "size": 10,
        "pretty": True,
        "dataset": "phone, mobile_phone",
    }
    with pytest.raises(ValidationError):
        client.person.search(**data)


@pytest.mark.usefixtures("client")
def test_api_endpoint_search_invalid_dataset_raises_validation_error(client):
    """
    Raises ValidationError with invalid dataset.
    """
    es_query = {
        "query": {
            "bool": {
                "must": [
                    {"term": {"location_country": "mexico"}},
                    {"term": {"job_title_role": "health"}}
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
        client.person.search(**data)
