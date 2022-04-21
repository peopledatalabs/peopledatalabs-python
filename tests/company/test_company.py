"""
All tests related to the Company object of the client instance.
"""


import logging
import pytest

from peopledatalabs.main import Company
from peopledatalabs.errors import InvalidEndpointError


logging.basicConfig()
logger = logging.getLogger("PeopleDataLabs.tests.company")


@pytest.mark.usefixtures("client_with_fake_api_key")
def test_init_company(client_with_fake_api_key):
    """
    Tests init of Company object as attribute of client object.
    """
    assert isinstance(client_with_fake_api_key.company, Company)


@pytest.mark.usefixtures("client_with_fake_api_key")
def test_calls_unsupported_endpoints(client_with_fake_api_key):
    """
    Tests calling undefined methods in Company raises InvalidEndpointError.
    """
    unsupported = [
        "autocomplete",
        "bulk",
        "identify",
        "retrieve",
    ]
    for method in unsupported:
        with pytest.raises(InvalidEndpointError):
            getattr(client_with_fake_api_key.company, method)()
