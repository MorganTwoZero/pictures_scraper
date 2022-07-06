import pytest

from fastapi.testclient import TestClient

from utils.request import request, request_homeline_many_users
from settings import settings


@pytest.mark.vcr
@pytest.fixture
def fetch_apis():
    pass