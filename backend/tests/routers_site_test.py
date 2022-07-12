import pytest

from fastapi.testclient import TestClient

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

    login = client.post(
        '/api/login', 
        data={'username': 'test', 'password': 'test'}
        )

    client.post(
        'http://localhost:8000/api/settings', 
        json={
            'user': 'test',
            'twitter_header': settings.TWITTER_HEADER,
            'authors_blacklist': '1',
            'tags_blacklist': '1',
        }, 
        cookies={
            'Authorization': login.cookies.get('Authorization'),
        },
    )

@pytest.mark.vcr
def test_site_like(
    create_user_with_twitter_header, client: TestClient):

    login = client.post(
        '/api/login', 
        data={'username': 'test', 'password': 'test'}
        )

    like = client.get(
        '/api/like?post_link=https://twitter.com/djamilaknopf/status/1537470332772274176/',
        cookies={
            'Authorization': login.cookies.get('Authorization')
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

    login = client.post(
        '/api/login', 
        data={'username': 'test', 'password': 'test'}
        )

    client.get('/api/update')
    client.get('/api/update')

    response = client.get('/api/myfeed',
        cookies={
            'Authorization': login.cookies.get('Authorization')
        }
    )

    assert response.status_code == 200
    assert response.json()