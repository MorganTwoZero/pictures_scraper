import pytest
import httpx

from db.schemas import RequestResults
from utils import request


@pytest.mark.vcr
async def test_request_honkai():
    assert type(await request.request_honkai()) == RequestResults

@pytest.mark.vcr
async def test_request_homeline(user_with_twitter):
    assert await request.request_homeline([user_with_twitter])

def test_request_urls_list():
    assert len(request.urls) == 4 + len(request.LOFTER_TAGS.split(' '))

@pytest.mark.vcr
async def test_request_get():
    client = httpx.AsyncClient()
    response = await request._get(client, 'https://jsonplaceholder.typicode.com/posts')
    assert response.status_code == 200

async def test_request_get_timeout():
    client = httpx.AsyncClient()
    response = await request._get(client, 'http://10.255.255.1')
    assert response.status_code == 400
    assert response.text == 'Request timeout'

@pytest.mark.vcr
async def test_request_pixiv_proxy():
    url = 'https://www.pixiv.net/touch/ajax/illust/details?illust_id=99572709'
    response = await request.pixiv_proxy(url)

    assert response.status_code == 200
    assert response.json().get('body')

@pytest.mark.vcr
async def test_request_like_request(user_with_twitter):
    post_id = 1600656404301328384
    like = await request.like_request(post_id, user_with_twitter)

    assert like.status_code == 403
    assert like.json()['errors'][0]['message'] == 'You have already favorited this status.'
