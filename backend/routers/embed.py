from fastapi import APIRouter, Response, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

from utils.pixiv_proxy_image import pixiv_proxy_image


router = APIRouter(
    prefix="/api/embed",
    tags=["embed"],
)

discord_useragent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11.6; rv:92.0) Gecko/20100101 Firefox/92.0'

@router.get('/{post_id}.jpg', response_class=Response)
async def img(request: Request, post_id: int, big: bool = True):
    '''Check if the user is accessing the embed from a discord client, 
    if so, send small image, else send big image'''
    if request.headers.get('user-agent') == discord_useragent:
        big = False
    image = await pixiv_proxy_image(post_id, big)
    return Response(content=image, media_type="image")

@router.get('/{post_id}.json', response_class=JSONResponse)
def json(post_id: int):

    url = "https://honkai-pictures.ru/api/embed/{post_id}.jpg".format(post_id=post_id)

    json = {
            "type": "image/jpeg",
            "url": url,
            "author_name": "Source",
            "author_url": "https://www.pixiv.net/en/artworks/{post_id}".format(post_id=post_id),
            "provider_name": "Pixiv",
        }

    return JSONResponse(content=json, media_type="application/json")

@router.get('/{post_id}')
def embed(request: Request, post_id: int):
    '''Check if the user is accessing the embed from a discord client,
    if not (i.e. directly from a browser) then redirect to the .jpg version'''
    if request.headers.get('user-agent') != discord_useragent:
        return RedirectResponse(url='https://honkai-pictures.ru/api/embed/{post_id}.jpg'.format(post_id=post_id))

    html = '''
    <html>
        <head>
            <link type="application/json+oembed" href="https://honkai-pictures.ru/api/embed/{post_id}.json"/>
            <meta name="twitter:card" content="summary_large_image">
            <meta name="twitter:image" content="https://honkai-pictures.ru/api/embed/{post_id}.jpg">
        </head>
    </html>
    '''.format(post_id=post_id)

    return HTMLResponse(content=html)
