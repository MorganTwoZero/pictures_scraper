import pytest

from fastapi.testclient import TestClient
from pydantic.error_wrappers import ValidationError

from settings import settings


@pytest.fixture
def create_user(client: TestClient):
    client.post(
        '/api/register', 
        data={'username': 'test', 'password': 'test'}
        )

def test_register(client: TestClient):

    register = client.post(
        '/api/register', 
        data={'username': 'test', 'password': 'test'}
        )

    assert register.status_code == 200

def test_register_empty_password(client: TestClient):

    with pytest.raises(ValidationError) as e:
        client.post(
            '/api/register', 
            data={'username': 'test', 'password': ''}
            )

def test_register_max_length(client: TestClient):

    register = client.post(
        '/api/register', 
        data={'username': 'test', 'password': 'x'*100}
    )

    assert register.status_code == 422
        
def test_register_existing_user(client: TestClient):

    client.post(
        '/api/register', 
        data={'username': 'test', 'password': 'test'}
    )    
    register = client.post(
        '/api/register', 
        data={'username': 'test', 'password': 'test'}
    )

    assert register.status_code == 400

def test_login(create_user, client: TestClient):

    login = client.post(
        '/api/login', 
        data={'username': 'test', 'password': 'test'}
        )

    assert login.status_code == 200

def test_login_max_length(create_user, client: TestClient):

    login = client.post(
        '/api/login', 
        data={'username': 'test', 'password': 'x'*100}
    )

    assert login.status_code == 422

def test_login_wrong_password(create_user, client: TestClient):

    login = client.post(
        '/api/login', 
        data={'username': 'test', 'password': 'wrong_test'}
    )

    assert login.status_code == 401

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