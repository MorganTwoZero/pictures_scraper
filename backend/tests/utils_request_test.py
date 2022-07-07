import pytest

from db.schemas import RequestResults, UserWithTwitter
from settings import settings
from utils import request


@pytest.fixture
def user_with_twitter():
    user = UserWithTwitter(
        username='test',
        twitter_header=settings.TWITTER_HEADER,
    )
    return user

@pytest.mark.vcr
async def test_request():
    assert type(await request.request_honkai()) == RequestResults

@pytest.mark.vcr
async def test_request_homeline(user_with_twitter):
    assert await request.request_homeline([user_with_twitter])