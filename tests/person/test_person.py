import logging
import pytest

from peopledatalabs_python.errors import EmptyParametersException


logging.basicConfig()
logger = logging.getLogger("PeopleDataLabs.tests")


@pytest.mark.usefixtures("client_with_fake_api_key")
def test_init_person(client_with_fake_api_key):
    person = client_with_fake_api_key.person
    logger.debug(person)


@pytest.mark.usefixtures("client_with_fake_api_key")
def test_enrichment_no_params_throw_error(client_with_fake_api_key):
    with pytest.raises(EmptyParametersException):
        client_with_fake_api_key.person.enrichment()
