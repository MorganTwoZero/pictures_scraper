import pytest

from fastapi.testclient import TestClient

from routers.embed import parse_post_id
from settings import settings


@pytest.mark.vcr
def test_embed(client: TestClient):
    '''Test if the embed returns image'''
    response = client.get('/api/embed/99083556')
    assert response.status_code == 200
    assert response.headers['content-type'] == 'image'

@pytest.mark.vcr
def test_embed_id_not_found(client: TestClient):
    '''Test if the embed returns image'''
    response = client.get('/api/embed/990835560')
    assert response.status_code == 404
    assert response.json() == {'error': 'Post not found, probably wrong id'}

@pytest.mark.vcr
def test_embed_id_not_int(client: TestClient):
    '''Test if the embed returns image'''
    response = client.get('/api/embed/9908355q')
    assert response.status_code == 422
    assert response.json() == {'error': 'Post id or pic number is not an integer'}

@pytest.mark.vcr
def test_embed_discord(client: TestClient):
    '''Test if the embed returns html with json for discord'''
    response = client.get(
        '/api/embed/99083556',
        headers={'user-agent': 'Mozilla/5.0 (compatible; Discordbot/2.0; +https://discordapp.com)'})
    assert response.status_code == 200
    assert response.headers['content-type'] == 'text/html; charset=utf-8'
    assert response.text.startswith('\n        <html>')
    assert response.text.endswith('</html>\n    ')
    assert settings.SITE_URL+'/api/embed/99083556.json' in response.text
    
@pytest.mark.vcr
def test_embed_json(client: TestClient):
    '''Test for the correct json'''
    response = client.get(
        '/api/embed/99083556.json',
        headers={'user-agent': 'Mozilla/5.0 (compatible; Discordbot/2.0; +https://discordapp.com)'})
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/json'
    assert response.json() == {
        'type':'image/jpeg',
        'url': settings.SITE_URL+'/api/embed/99083556.jpg',
        'author_name':'Source',
        'author_url':'https://www.pixiv.net/en/artworks/99083556'
        }

@pytest.mark.parametrize('requested_id, post_id, pic_num', [
    ('99487795_p1', 99487795, 1),
    ('99487795_p0', 99487795, 0),
    ('99487795', 99487795, 0),
])
def test_embed_parse_id(
    requested_id: str, 
    post_id: int, 
    pic_num: int
    ):
    parsed_id, parsed_pic_num = parse_post_id(requested_id)
    assert parsed_id == post_id
    assert parsed_pic_num == pic_num

@pytest.mark.parametrize('requested_id', [
    'string',
    '99487795_p',
    '99487795_pq',
    'qwer_p1',
    '_p1',
])
def test_embed_invalid_parse_id(requested_id: str):

    with pytest.raises(ValueError):
        parse_post_id(requested_id)

@pytest.mark.parametrize('user_agent, status_code', [
    ('Mozilla/5.0 (compatible; Discordbot/2.0; +https://discordapp.com)', 200),
    ('Mozilla/5.0 (Macintosh; Intel Mac OS X 11.6; rv:92.0) Gecko/20100101 Firefox/92.0', 200),
])
def test_embed_discord_useragent(client: TestClient, user_agent: str, status_code: int):
    '''Test for discord`s client/crawler detection'''
    request = client.get(
        '/api/embed/99083556',
        allow_redirects=False,
        headers={'user-agent': user_agent},
    )

    assert request.status_code == status_code

def test_embed_not_discord_useragent(client: TestClient):
    request = client.get(
        '/api/embed/99083556',
        allow_redirects=False,
        headers={'user-agent': ''},
    )

    assert request.status_code == 307