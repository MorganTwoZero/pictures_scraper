from fastapi.testclient import TestClient


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
            'twitter_header': "{'cookie': 'auth_token=32f0ea53e854116ac76a61b5f056f62cc085894c; ct0=99564d182d20e3f98dca1a08782829a0ac2760d03eb807f5fd248ea319fa3fc5a25eb19ba72f6149a0716efa51b580fcc1aebf9afcc8fa2b6e761ebc4b017584ac5a2d09e0a9a6b4ac801b597b4286e2', 'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA', 'x-csrf-token': '99564d182d20e3f98dca1a08782829a0ac2760d03eb807f5fd248ea319fa3fc5a25eb19ba72f6149a0716efa51b580fcc1aebf9afcc8fa2b6e761ebc4b017584ac5a2d09e0a9a6b4ac801b597b4286e2'}",
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

    settings = client.post(
        'http://localhost:8000/api/settings', 
        json=settings_json, 
        cookies={
            'Authorization': login.cookies.get('Authorization'),
        },
        )

    assert settings.status_code == 200
    assert settings.json()['message'] == 'Settings updated successfully'

def test_saved_settings(client: TestClient):

    settings_json = {
            'user': 'test',
            'twitter_header': "{'cookie': 'auth_token=32f0ea53e854116ac76a61b5f056f62cc085894c; ct0=99564d182d20e3f98dca1a08782829a0ac2760d03eb807f5fd248ea319fa3fc5a25eb19ba72f6149a0716efa51b580fcc1aebf9afcc8fa2b6e761ebc4b017584ac5a2d09e0a9a6b4ac801b597b4286e2', 'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA', 'x-csrf-token': '99564d182d20e3f98dca1a08782829a0ac2760d03eb807f5fd248ea319fa3fc5a25eb19ba72f6149a0716efa51b580fcc1aebf9afcc8fa2b6e761ebc4b017584ac5a2d09e0a9a6b4ac801b597b4286e2'}",
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