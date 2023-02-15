import pytest
from datetime import datetime, timezone
from fastapi.testclient import TestClient

from routers.site import set_update_time, last_update_time
from settings import settings


@pytest.mark.vcr
@pytest.fixture
def fill_db_with_posts(client: TestClient):
    client.get('/api/update')

@pytest.fixture
def create_user_with_twitter_header(client: TestClient):

    client.post(
        '/api/register',
        data={'username': 'test', 'password': 'test'}
        )

    login_cookie = client.post(
        '/api/login', 
        data={'username': 'test', 'password': 'test'}
        ).cookies["Authorization"]

    client.post(
        'http://localhost:8000/api/settings', 
        json={
            'user': 'test',
            'twitter_header': settings.TWITTER_HEADER,
            'authors_blacklist': '1',
            'tags_blacklist': '1',
        }, 
        cookies={
            'Authorization': login_cookie
        },
    )

@pytest.mark.vcr
def test_site_like(
    create_user_with_twitter_header, client: TestClient):

    login_cookie = client.post(
        '/api/login', 
        data={'username': 'test', 'password': 'test'}
        ).cookies["Authorization"]

    like = client.get(
        "/api/like?post_link=https://twitter.com/OZcellt/status/1625362770215735301/",
        cookies={
            'Authorization': login_cookie
        }    
    )

    assert like.status_code == 200
    assert like.json()['status'] == 403
    assert like.json()['twitter_json']['errors'][0]['message'] == 'You have already favorited this status.'

@pytest.mark.vcr
def test_site_honkai(fill_db_with_posts, client: TestClient):

    response = client.get('/api/honkai')

    assert response.status_code == 200
    assert response.json()

@pytest.mark.vcr
def test_site_homeline(
    create_user_with_twitter_header, client: TestClient):

    login_cookie = client.post(
        '/api/login', 
        data={'username': 'test', 'password': 'test'}
        ).cookies["Authorization"]

    client.get('/api/update')
    client.get('/api/update')

    response = client.get('/api/myfeed',
        cookies={
            'Authorization': login_cookie
        }
    )

    assert response.status_code == 200
    assert response.json()

@pytest.mark.vcr
async def test_last_update():
    set_update_time()
    last_update = await last_update_time()
    now = datetime.now(tz=timezone.utc)
    assert last_update == now