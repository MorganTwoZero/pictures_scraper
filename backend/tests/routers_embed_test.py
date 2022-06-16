import pytest


def test_embed(client):
    '''Test if the embed returns image'''
    response = client.get('/api/embed/99083556')
    assert response.status_code == 200
    assert response.headers['content-type'] == 'image'

@pytest.mark.parametrize('pic_id, expected_status_code, expected_json', [
    ('990835560', 200, {'error': ''}),
    ('9908355q', 422, {'detail': [{'loc': ['path', 'post_id'],
   'msg': 'value is not a valid integer',
   'type': 'type_error.integer'}]}),
    ])
def test_wrong_id_(client, pic_id, expected_status_code, expected_json):
    '''Test if the embed returns image'''
    response = client.get('/api/embed/{pic_id}'.format(pic_id=pic_id))
    assert response.status_code == expected_status_code
    assert response.json() == expected_json

def test_embed_discord(client):
    '''Test if the embed returns html with json for discord'''
    response = client.get(
        '/api/embed/99083556',
        headers={'user-agent': 'Mozilla/5.0 (compatible; Discordbot/2.0; +https://discordapp.com)'})
    assert response.status_code == 200
    assert response.headers['content-type'] == 'text/html; charset=utf-8'
    assert response.text.startswith('\n        <html>')
    assert response.text.endswith('</html>\n    ')
    assert 'https://honkai-pictures.ru/api/embed/99083556.json' in response.text
    
def test_embed_json(client):
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