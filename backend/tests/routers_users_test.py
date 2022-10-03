import pytest
from datetime import datetime, timedelta
from requests import Response

from fastapi.testclient import TestClient
from pydantic.error_wrappers import ValidationError

from settings import settings


@pytest.fixture
def create_user(client: TestClient):
    client.post(
        '/api/register', 
        data={'username': 'test', 'password': 'test'}
        )

@pytest.fixture
def login(client: TestClient):
    login = client.post(
        '/api/login', 
        data={'username': 'test', 'password': 'test'}
        )
    return login

settings_json = {
            'user': 'test',
            'twitter_header': settings.TWITTER_HEADER,
            'authors_blacklist': '1',
            'tags_blacklist': '1',
        }

def test_users_register(client: TestClient):

    register = client.post(
        '/api/register', 
        data={'username': 'test', 'password': 'test'}
        )

    assert register.status_code == 200

def test_users_register_empty_password(client: TestClient):

    with pytest.raises(ValidationError):
        client.post(
            '/api/register', 
            data={'username': 'test', 'password': ''}
            )

def test_users_register_password_max_length(
    client: TestClient):

    register = client.post(
        '/api/register', 
        data={'username': 'test', 'password': 'x'*100}
    )

    assert register.status_code == 422

def test_users_register_username_max_length(
    client: TestClient):

    register = client.post(
        '/api/register', 
        data={'username': 'test'*100, 'password': 'x'}
    )

    assert register.status_code == 422
        
def test_users_register_existing_user(client: TestClient):

    client.post(
        '/api/register', 
        data={'username': 'test', 'password': 'test'}
    )    
    register = client.post(
        '/api/register', 
        data={'username': 'test', 'password': 'test'}
    )

    assert register.status_code == 400

def test_users_login(create_user, client: TestClient):

    login = client.post(
        '/api/login', 
        data={'username': 'test', 'password': 'test'}
        )

    assert login.status_code == 200

def test_users_login_password_max_length(
    create_user, client: TestClient):

    login = client.post(
        '/api/login', 
        data={'username': 'test', 'password': 'x'*100}
    )

    assert login.status_code == 422

def test_users_login_username_max_length(
    create_user, client: TestClient):

    login = client.post(
        '/api/login', 
        data={'username': 'test'*100, 'password': 'x'}
    )

    assert login.status_code == 422

def test_users_login_wrong_password(
    create_user, client: TestClient):

    login = client.post(
        '/api/login', 
        data={'username': 'test', 'password': 'wrong_test'}
    )

    assert login.status_code == 401

def test_users_settings(
    create_user, login: Response, client: TestClient):

    settings_response = client.post(
        'api/settings', 
        json=settings_json, 
        cookies={
            'Authorization': login.cookies.get('Authorization'),
        },
    )

    assert settings_response.status_code == 200
    assert settings_response.json()['message'] == 'Settings updated successfully'

def test_users_settings_no_auth(
    create_user, login: Response, client: TestClient):

    settings_response = client.post(
        'api/settings', 
        json=settings_json,
    )

    assert settings_response.status_code == 401
    assert settings_response.json()['detail'] == 'Could not validate credentials'

def test_users_settings_wrong_data(
    create_user, login: Response, client: TestClient):

    settings_response = client.post(
        'api/settings', 
        json={
            'user': 'wrong',
            'twitter_header': settings.TWITTER_HEADER,
            'authors_blacklist': '1',
            'tags_blacklist': '1',
        }, 
        cookies={
            'Authorization': login.cookies.get('Authorization'),
        },
        )

    assert settings_response.status_code == 400
    assert settings_response.json()['detail'] == 'Wrong username'

def test_users_settings_empty_data(
    create_user, login: Response, client: TestClient):

    settings_response = client.post(
        'api/settings',
        cookies={
            'Authorization': login.cookies.get('Authorization'),
        },
        )

    assert settings_response.status_code == 422

def test_users_settings_changes(
    create_user, login: Response, client: TestClient):

    client.post(
        'api/settings', 
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

def test_users_logout(
    create_user, login: Response, client: TestClient):

    logout = client.get(
        'api/logout',
        cookies={
            'Authorization': login.cookies.get('Authorization'),
        },
    )

    assert logout.json()['message'] == 'Logged out'
    assert len(logout.cookies) == 0


def test_users_cookie_username(
    create_user, login: Response, client: TestClient):
    assert login.cookies['username'] == 'test'

def test_users_cookie_expires(
    create_user, login: Response, client: TestClient):

    expires_delta = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expected_expires = int(datetime.timestamp(
        datetime.now() + expires_delta
        ))

    expires = None
    for cookie in login.cookies:
        if cookie.name == 'Authorization':
            expires = cookie.expires

    assert expires == expected_expires

def test_users_cookie_httponly(
    create_user, login: Response, client: TestClient):

    for cookie in login.cookies:
        if cookie.name == 'Authorization':
            assert 'HttpOnly' in cookie._rest  # type: ignore

def test_users_cookie_secure(
    create_user, login: Response, client: TestClient):

    for cookie in login.cookies:
        if cookie.name == 'Authorization':
            assert cookie.secure