"""
All tests related to the Person object of the client instance.
"""

import logging
import pytest

from peopledatalabs.main import Person


logging.basicConfig()
logger = logging.getLogger("PeopleDataLabs.tests.person")


@pytest.mark.usefixtures("client_with_fake_api_key")
def test_init_person(client_with_fake_api_key):
    """
    Tests init of Person object as attribute of client object.
    """
    assert isinstance(client_with_fake_api_key.person, Person)
