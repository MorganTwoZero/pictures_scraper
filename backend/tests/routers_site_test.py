from fastapi.testclient import TestClient


def test_like(client: TestClient):

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
            'twitter_header': "{'cookie': 'auth_token=32f0ea53e854116ac76a61b5f056f62cc085894c; ct0=99564d182d20e3f98dca1a08782829a0ac2760d03eb807f5fd248ea319fa3fc5a25eb19ba72f6149a0716efa51b580fcc1aebf9afcc8fa2b6e761ebc4b017584ac5a2d09e0a9a6b4ac801b597b4286e2', 'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA', 'x-csrf-token': '99564d182d20e3f98dca1a08782829a0ac2760d03eb807f5fd248ea319fa3fc5a25eb19ba72f6149a0716efa51b580fcc1aebf9afcc8fa2b6e761ebc4b017584ac5a2d09e0a9a6b4ac801b597b4286e2'}",
            'authors_blacklist': '1',
            'tags_blacklist': '1',
        }, 
        cookies={
            'Authorization': login.cookies.get('Authorization'),
        },
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