import re
from typing import NamedTuple
import logging

from fastapi import APIRouter, Request, Response, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse

from utils.pixiv_proxy_image import pixiv_proxy_image


SITE_URL = 'https://www.pixiv.sbs/en/artworks'

router = APIRouter(
    prefix="/en/artworks",
    tags=["embed"],
)

logger = logging.getLogger(__name__)

class ParsedPostId(NamedTuple):
    post_id: int
    pic_num: int

def _discord(request: Request) -> bool:

    discord_useragent = [
        'Mozilla/5.0 (compatible; Discordbot/2.0; +https://discordapp.com)',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 11.6; rv:92.0) Gecko/20100101 Firefox/92.0',
        ]

    return request.headers.get('user-agent') in discord_useragent

def parse_post_id(requested_id: str) -> ParsedPostId:
    '''Ищем _p, если есть - всё что до него это id поста, всё что после - номер пикчи.\n
    Если не находим, то вся строка и есть id поста, а номер пикчи = 0'''

    search = re.search('_p', requested_id)
    if search:
        post_id = int(requested_id[:search.start()])
        pic_num = int(requested_id[search.end():])
        return ParsedPostId(post_id, pic_num)

    return ParsedPostId(int(requested_id), 0)

@router.get('/{requested_id}.jpg')
async def img(request: Request, requested_id: str, is_big: bool | None = None):
    '''Check if a user is accessing the embed from a discord client, 
    if so, send small image, else send is_big image. By default return small pic.'''

    logger.debug(
        "Image requested, requested_id={}, user_agent={}".format(requested_id,request.headers.get('user-agent'))
    )

    if is_big is None:
        is_big = True
    
    if _discord(request):
        is_big = False

    try:
        post_id, pic_num = parse_post_id(requested_id)
    except ValueError:
        raise HTTPException(422, 'Post id or pic number is not an integer')

    try:
        image = await pixiv_proxy_image(post_id, pic_num, is_big)
    except HTTPException:
        logger.exception('Embed error')
        raise

    if image is None:
        raise HTTPException(404, 'Post not found, probably wrong id')

    return Response(content=image, media_type="image")

@router.get('/{requested_id}.json')
async def redirect(request: Request, requested_id: str):
    #return RedirectResponse(str(request.url) + '.jpg')

    json = {
            "type": "image/jpeg",
            "url": SITE_URL+'/{requested_id}.jpg'.format(requested_id=requested_id)
        }
    return json

@router.get('/{requested_id}')
def html(request: Request, requested_id: str, is_big: bool | None = None):
    '''Check if a user is accessing the embed from a discord client,
    if not (i.e. directly from a browser) then redirect to the .jpg version.'''

    logger.debug(
        "Embed requested, requested_id={}, user_agent={}".format(requested_id,request.headers.get('user-agent'))
    )

    if not _discord(request):
        return RedirectResponse(url=SITE_URL+'/{requested_id}.jpg'.format(requested_id=requested_id))

    html = '''
        <html>
            <head>
                <link type="application/json+oembed" href="{SITE_URL}/{requested_id}.json"/>
                <meta name="twitter:card" content="summary_large_image">
                <meta name="twitter:image" content="{SITE_URL}/{requested_id}.jpg">
            </head>
        </html>
    '''.format(requested_id=requested_id, SITE_URL=SITE_URL)

    return HTMLResponse(content=html)