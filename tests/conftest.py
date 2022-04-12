import uuid

import pytest

from peopledatalabs_python.main import PDLPY
from peopledatalabs_python.logger import get_logger


logger = get_logger("tests")


@pytest.fixture
def fake_api_key():
    return str(uuid.uuid4())


@pytest.fixture
def client():
    client = PDLPY()
    logger.debug(f"client: {client}")
    return client


@pytest.fixture
def client_with_fake_api_key(fake_api_key):
    client = PDLPY(api_key=fake_api_key)
    logger.debug(f"client: {client}")
    return client
