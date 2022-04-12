import logging
import pytest

from peopledatalabs_python.errors import EmptyParametersException
from peopledatalabs_python.main import Person


logging.basicConfig()
logger = logging.getLogger("PeopleDataLabs.tests")


@pytest.mark.usefixtures("client_with_fake_api_key")
def test_init_person(client_with_fake_api_key):
    assert isinstance(client_with_fake_api_key.person, Person)


@pytest.mark.usefixtures("client_with_fake_api_key")
def test_enrichment_no_params_raises_EmptyParametersException(
    client_with_fake_api_key
):
    with pytest.raises(EmptyParametersException):
        client_with_fake_api_key.person.enrichment()


@pytest.mark.usefixtures("client")
def test_enrichment_api_endpoint(client):
    enriched = client.person.enrichment(
        profile="https://www.linkedin.com/in/guido-van-rossum-4a0756/"
    )
    assert enriched.status_code == 200
