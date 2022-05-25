from fastapi import APIRouter, Response
from fastapi.responses import HTMLResponse, JSONResponse

from utils.pixiv_proxy_image import pixiv_proxy_image


router = APIRouter(
    prefix="/api/embed",
    tags=["embed"],
)

@router.get('/{post_id}.jpg', response_class=Response)
async def img(post_id: int, big: bool = False):
    image = await pixiv_proxy_image(post_id, big)
    return Response(content=image, media_type="image")

@router.get('/{post_id}.json', response_class=JSONResponse)
def json(post_id: int, big: bool = False):

    url = "https://honkai-pictures.ru/api/embed/{post_id}.jpg?big={big}".format(post_id=post_id, big=big)

    json = {
            "type": "image/jpeg",
            "url": url,
            "author_name": "Source",
            "author_url": "https://www.pixiv.net/en/artworks/{post_id}".format(post_id=post_id),
            "provider_name": "Pixiv",
        }

    return JSONResponse(content=json, media_type="application/json")

@router.get('/{post_id}', response_class=HTMLResponse)
def embed(post_id: int, big: bool = False):

    html = '''
    <html>
        <head>
            <link type="application/json+oembed" href="https://honkai-pictures.ru/api/embed/{post_id}.json?big={big}"/>
            <meta name="twitter:card" content="summary_large_image">
            <meta name="twitter:image" content="https://honkai-pictures.ru/api/embed/{post_id}.jpg?big={big}">
        </head>
    </html>
    '''.format(post_id=post_id, big=big)

    return HTMLResponse(content=html)
