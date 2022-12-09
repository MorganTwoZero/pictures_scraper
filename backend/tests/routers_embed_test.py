from typing import Any
from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from requests.structures import CaseInsensitiveDict

from settings import settings
from routers.embed import router as embed_router
from routers.embed import parse_post_id
from main import app


header = CaseInsensitiveDict(
    {'user-agent': 'Mozilla/5.0 (compatible; Discordbot/2.0; +https://discordapp.com)'}
    )

@pytest.fixture(scope="function")
def client(app: FastAPI) -> Generator[TestClient, Any, None]:
    with TestClient(app) as client:
        client.headers = header # type: ignore        
        yield client


SITE_URL = settings.SITE_URL + '/en/artworks'

@pytest.mark.vcr
def test_embed_redirect(client: TestClient):
    response = client.get(
        '/en/artworks/99083556', 
        headers={'user-agent': ''},
        allow_redirects=False
        )
    assert response.is_redirect

@pytest.mark.vcr
def test_embed_id_not_int(client: TestClient):
    response = client.get('/en/artworks/9908355q')
    assert response.status_code == 400
    assert 'Cannot parse post id' in response.text

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
    '''Test for discord's client/crawler detection'''
    request = client.get(
        '/en/artworks/99083556',
        allow_redirects=False,
        headers={'user-agent': user_agent},
    )

    assert request.status_code == status_code

def test_embed_not_discord_useragent(client: TestClient):
    request = client.get(
        '/en/artworks/99083556',
        allow_redirects=False,
        headers={'user-agent': ''},
    )

    assert request.status_code == 307