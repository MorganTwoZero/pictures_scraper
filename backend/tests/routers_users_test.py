from fastapi.testclient import TestClient

from settings import settings


def test_register(client: TestClient):

    register = client.post(
        '/api/register', 
        data={'username': 'test', 'password': 'test'}
        )

    assert register.status_code == 200

def test_login(client: TestClient):

    client.post(
        '/api/register',
        data={'username': 'test', 'password': 'test'}
        )

    login = client.post(
        '/api/login', 
        data={'username': 'test', 'password': 'test'}
        )

    assert login.status_code == 200

def test_settings(client: TestClient):

    settings_json = {
            'user': 'test',
            'twitter_header': settings.TWITTER_HEADER,
            'authors_blacklist': '1',
            'tags_blacklist': '1',
        }

    client.post(
        '/api/register',
        data={'username': 'test', 'password': 'test'}
        )

    login = client.post(
        '/api/login', 
        data={'username': 'test', 'password': 'test'}
        )

    settings_response = client.post(
        'http://localhost:8000/api/settings', 
        json=settings_json, 
        cookies={
            'Authorization': login.cookies.get('Authorization'),
        },
        )

    assert settings_response.status_code == 200
    assert settings_response.json()['message'] == 'Settings updated successfully'

def test_saved_settings(client: TestClient):

    settings_json = {
            'user': 'test',
            'twitter_header': settings.TWITTER_HEADER,
            'authors_blacklist': '1',
            'tags_blacklist': '1',
        }

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
        json=settings_json, 
        cookies={
            'Authorization': login.cookies.get('Authorization'),
        },
        )

    saved_settings = client.get('/api/user', cookies={
        'Authorization': login.cookies.get('Authorization'),
    })

    assert saved_settings.status_code == 200
    assert saved_settings.json() == settings_json