"""
All tests related to the Company object of the client instance.
"""


import logging
import pytest

from peopledatalabs_python.main import Company


logging.basicConfig()
logger = logging.getLogger("PeopleDataLabs.tests.company")


@pytest.mark.usefixtures("client_with_fake_api_key")
def test_init_company(client_with_fake_api_key):
    """
    Tests init of Company object as attribute of client object.
    """
    assert isinstance(client_with_fake_api_key.company, Company)
