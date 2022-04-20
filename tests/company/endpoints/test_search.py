"""
Tests calls to the company/search API.
"""


import logging
import pytest

from pydantic import ValidationError
import requests

from peopledatalabs.errors import EmptyParametersException


logging.basicConfig()
logger = logging.getLogger("PeopleDataLabs.tests.company.search")


@pytest.mark.usefixtures("client_with_fake_api_key")
def test_search_empty_params_throw_error(client_with_fake_api_key):
    """
    Tests calling the search method without parameters.

    Should raise EmptyParametersException
    """
    with pytest.raises(EmptyParametersException):
        client_with_fake_api_key.company.search()


@pytest.mark.usefixtures("client")
def test_api_endpoint_search_query(client):
    """
    Tests successful execution of search API by ES query.
    """
    es_query = {
        "query": {
            "bool": {
                "must": [
                    {"term": {"tags": "big data"}},
                    {"term": {"industry": "financial services"}},
                    {"term": {"location.country": "united states"}},
                ]
            }
        }
    }
    data = {
        "query": es_query,
        "size": 10,
        "pretty": True,
    }
    response = client.company.search(**data)
    assert isinstance(response, requests.Response)
    assert response.status_code == 200


@pytest.mark.usefixtures("client")
def test_api_endpoint_search_sql(client):
    """
    Tests successful execution of search API by SQL query.
    """
    sql_query = (
        "SELECT * FROM company"
        " WHERE tags='big data'"
        " AND industry='financial services'"
        " AND location.country='united states';"
    )
    data = {
        "sql": sql_query,
        "size": 10,
        "pretty": True,
    }
    response = client.company.search(**data)
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
                    {"term": {"tags": "big data"}},
                    {"term": {"industry": "financial services"}},
                    {"term": {"location.country": "united states"}},
                ]
            }
        }
    }
    sql_query = (
        "SELECT * FROM company"
        "WHERE tags='big data'"
        "AND industry='financial services'"
        "AND location.country='united states';"
    )
    data = {
        "query": es_query,
        "sql": sql_query,
        "size": 10,
        "pretty": True,
        "dataset": "phone, mobile_phone",
    }
    with pytest.raises(ValidationError):
        client.company.search(**data)
