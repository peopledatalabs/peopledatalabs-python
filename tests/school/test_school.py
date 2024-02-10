"""
All tests related to the School object of the client instance.
"""

import logging
import pytest

from peopledatalabs.main import School
from peopledatalabs.errors import InvalidEndpointError


logging.basicConfig()
logger = logging.getLogger("PeopleDataLabs.tests.school")


@pytest.mark.usefixtures("client_with_fake_api_key")
def test_init_school(client_with_fake_api_key):
    """
    Tests init of School object as attribute of client object.
    """
    assert isinstance(client_with_fake_api_key.school, School)


# pylint: disable=duplicate-code
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
        "skill",
        "job_title",
        "ip",
    ]
    for method in unsupported:
        with pytest.raises(InvalidEndpointError):
            getattr(client_with_fake_api_key.school, method)()
