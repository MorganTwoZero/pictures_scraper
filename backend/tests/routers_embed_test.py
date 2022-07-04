import pytest

from fastapi.testclient import TestClient

from routers.embed import parse_post_id


@pytest.mark.vcr
def test_embed(client: TestClient):
    '''Test if the embed returns image'''
    response = client.get('/api/embed/99083556')
    assert response.status_code == 200
    assert response.headers['content-type'] == 'image'

@pytest.mark.vcr
@pytest.mark.parametrize('pic_id, expected_status_code, expected_json', [
    ('990835560', 404, {'error': 'Post not found, probably wrong id'}),
    ('9908355q', 422, {'error': 'Post id or pic number is not an integer'}),
    ])
@pytest.mark.vcr
def test_embed_wrong_id(client: TestClient, pic_id: int, expected_status_code: int, expected_json: dict[str, str]):
    '''Test if the embed returns image'''
    response = client.get('/api/embed/{pic_id}'.format(pic_id=pic_id))
    assert response.status_code == expected_status_code
    assert response.json() == expected_json

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
    assert 'https://honkai-pictures.ru/api/embed/99083556.json' in response.text
    
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
        'url':'https://honkai-pictures.ru/api/embed/99083556.jpg',
        'author_name':'Source',
        'author_url':'https://www.pixiv.net/en/artworks/99083556'
        }

@pytest.mark.parametrize('requested_id, post_id, pic_num', [
    ('99487795_p1', 99487795, 1),
    ('99487795_p0', 99487795, 0),
    ('99487795', 99487795, 0),
    pytest.param('string', 1, 1, marks=pytest.mark.xfail)
])
def test_embed_parse_id(
    requested_id: str, 
    post_id: int, 
    pic_num: int
    ):
    parsed_id, parsed_pic_num = parse_post_id(requested_id)
    assert parsed_id == post_id
    assert parsed_pic_num == pic_num

@pytest.mark.parametrize('user_agent, status_code', [
    ('Mozilla/5.0 (compatible; Discordbot/2.0; +https://discordapp.com)', 200),
    ('Mozilla/5.0 (Macintosh; Intel Mac OS X 11.6; rv:92.0) Gecko/20100101 Firefox/92.0', 200),
    ('', 307),
])
def test_embed_discord_useragent(client: TestClient, user_agent: str, status_code: int):
    '''Test for discord`s client/crawler detection'''
    request = client.get(
        '/api/embed/99083556',
        allow_redirects=False,
        headers={'user-agent': user_agent},
    )

    assert request.status_code == status_code