"""
All tests related to the Location object of the client instance.
"""


import logging
import pytest

from peopledatalabs_python.main import Location
from peopledatalabs_python.errors import InvalidEndpointError


logging.basicConfig()
logger = logging.getLogger("PeopleDataLabs.tests.location")


@pytest.mark.usefixtures("client_with_fake_api_key")
def test_init_location(client_with_fake_api_key):
    """
    Tests init of Location object as attribute of client object.
    """
    assert isinstance(client_with_fake_api_key.location, Location)


@pytest.mark.usefixtures("client_with_fake_api_key")
def test_calls_unsupported_endpoints(client_with_fake_api_key):
    """
    Tests calling undefined methods in School raises InvalidEndpointError.
    """
    unsupported = [
        "autocomplete",
        "bulk",
        "identify",
        "retrieve",
        "search",
    ]
    for method in unsupported:
        with pytest.raises(InvalidEndpointError):
            getattr(client_with_fake_api_key.location, method)()
