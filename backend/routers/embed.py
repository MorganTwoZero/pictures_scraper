import re
from typing import NamedTuple
import logging

from fastapi import APIRouter, Request, Response, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

from utils.pixiv_proxy_image import pixiv_proxy_image
from settings import settings


SITE_URL = settings.SITE_URL

router = APIRouter(
    prefix="/api/embed",
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

@router.get('/{requested_id}.jpg', response_class=Response)
async def img(request: Request, requested_id: str, is_big: bool = True):
    '''Check if a user is accessing the embed from a discord client, 
    if so, send small image, else send is_big image'''

    logger.debug(
        "Image requested, requested_id={}, user_agent={}".format(requested_id,request.headers.get('user-agent'))
    )
    
    if _discord(request):
        is_big = False

    try:
        post_id, pic_num = parse_post_id(requested_id)
    except ValueError:
        return JSONResponse({"error": "Post id or pic number is not an integer"}, status_code=422)

    try:
        image = await pixiv_proxy_image(post_id, pic_num, is_big)
    except HTTPException as e:
        logger.exception('Embed error')
        return JSONResponse({"error": e.detail}, status_code=500)

    if image is None:
        return JSONResponse({"error": "Post not found, probably wrong id"}, status_code=404)

    return Response(content=image, media_type="image")

@router.get('/{requested_id}.json', response_class=JSONResponse)
def json(requested_id: str):
    '''Json for cool embed'''

    try:
        post_id = parse_post_id(requested_id).post_id
    except ValueError:
        return JSONResponse({"error": "Post id is not an integer"}, status_code=422)
    
    url = SITE_URL+"/api/embed/{requested_id}.jpg".format(requested_id=requested_id)

    json = {
            "type": "image/jpeg",
            "url": url,
            "author_name": "Source",
            "author_url": "https://www.pixiv.net/en/artworks/{post_id}".format(post_id=post_id),
        }

    return JSONResponse(content=json, media_type="application/json")

@router.get('/{requested_id}')
def html(request: Request, requested_id: str):
    '''Check if a user is accessing the embed from a discord client,
    if not (i.e. directly from a browser) then redirect to the .jpg version.'''

    logger.debug(
        "Embed requested, requested_id={}, user_agent={}".format(requested_id,request.headers.get('user-agent'))
    )

    if not _discord(request):
        return RedirectResponse(url=SITE_URL+'/api/embed/{requested_id}.jpg'.format(requested_id=requested_id))

    html = '''
        <html>
            <head>
                <link type="application/json+oembed" href="{SITE_URL}/api/embed/{requested_id}.json"/>
                <meta name="twitter:card" content="summary_large_image">
                <meta name="twitter:image" content="{SITE_URL}/api/embed/{requested_id}.jpg">
            </head>
        </html>
    '''.format(requested_id=requested_id, SITE_URL=SITE_URL)

    return HTMLResponse(content=html)