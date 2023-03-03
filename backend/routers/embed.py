import logging
import re
from typing import NamedTuple

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from httpx import AsyncClient

from deps import get_request_client
from settings import settings
from utils.pixiv_proxy_image import pixiv_proxy_image

SITE_URL = settings.SITE_URL + '/en/artworks'

router = APIRouter(
    prefix="/en/artworks",
    tags=["embed"],
)

logger = logging.getLogger(__name__)

class ParsedPostId(NamedTuple):
    post_id: int
    pic_num: int

def is_discord(request: Request) -> bool:
    discord_useragent = [
        'Mozilla/5.0 (compatible; Discordbot/2.0; +https://discordapp.com)',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 11.6; rv:92.0) Gecko/20100101 Firefox/92.0',
        ]
    return bool(request.headers["User-Agent"] in discord_useragent)

def parse_post_id(requested_id: str) -> ParsedPostId:
    separator = re.search('_p', requested_id)
    if separator:
        post_id = int(requested_id[:separator.start()])
        pic_num = int(requested_id[separator.end():])
        return ParsedPostId(post_id, pic_num)

    return ParsedPostId(int(requested_id), 0)

@router.get('/{requested_id}.jpg')
async def img(requested_id: str, client: AsyncClient = Depends(get_request_client)) -> Response:
    post_id, pic_num = parse_post_id(requested_id)
    image = await pixiv_proxy_image(post_id, pic_num, client)
    if image is None:
        return Response("Failed to fetch the image", 500)
    return Response(content=image.content, media_type="image/jpeg")

@router.get('/{requested_id}')
def html(request: Request, requested_id: str) -> Response:
    success_html = '''
        <meta name="twitter:card" content="summary_large_image">
        <meta name="twitter:image" content="{SITE_URL}/{requested_id}.jpg">'''
    error_html = '<meta property="twitter:title" content="{}">'

    try:
        post_id, _ = parse_post_id(requested_id)
    except ValueError:
        return HTMLResponse(error_html.format('Cannot parse post id'), 400)

    if not is_discord(request):
        return RedirectResponse(url='https://www.pixiv.net/en/artworks'+f'/{post_id}')

    return HTMLResponse(
        content=success_html.format(
            requested_id=requested_id, 
            SITE_URL=SITE_URL.replace('//', '//www.')
        )
    )