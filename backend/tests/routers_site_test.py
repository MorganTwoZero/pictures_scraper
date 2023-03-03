import pytest
from datetime import datetime, timezone
from fastapi.testclient import TestClient

from routers.site import set_update_time, last_update_time


@pytest.mark.vcr
@pytest.fixture
def fill_db_with_posts(client: TestClient):
    client.get('/api/update')

@pytest.mark.vcr
def test_site_like(client: TestClient):
    like = client.get(
        "/api/like?post_link=https://twitter.com/OZcellt/status/1625362770215735301/", 
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
def test_site_homeline(fill_db_with_posts, client: TestClient):
    response = client.get('/api/myfeed')
    assert response.status_code == 200
    assert response.json()

@pytest.mark.vcr
async def test_last_update():
    set_update_time()
    last_update = await last_update_time()
    now = datetime.now(tz=timezone.utc)
    assert last_update == now