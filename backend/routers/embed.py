from fastapi import APIRouter, Request, Response, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

from utils.pixiv_proxy_image import pixiv_proxy_image


router = APIRouter(
    prefix="/api/embed",
    tags=["embed"],
)

discord_useragent = [
    'Mozilla/5.0 (compatible; Discordbot/2.0; +https://discordapp.com)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11.6; rv:92.0) Gecko/20100101 Firefox/92.0',
    ]

@router.get('/{pic_id}.jpg', response_class=Response)
async def img(request: Request, pic_id: str, big: bool = True):
    '''Check if a user is accessing the embed from a discord client, 
    if so, send small image, else send big image'''
    
    if request.headers.get('user-agent') in discord_useragent:
        big = False

    try:
        image = await pixiv_proxy_image(pic_id, big)
    except HTTPException as e:
        return JSONResponse({"error": str(e)})
    return Response(content=image, media_type="image")

@router.get('/{pic_id}.json', response_class=JSONResponse)
def json(pic_id: str):
    '''Json for cool embed'''

    if pic_id[-3:-1] == '_p':
        post_id = pic_id[:-3]
    else:
        post_id = pic_id
    
    url = "https://honkai-pictures.ru/api/embed/{pic_id}.jpg".format(pic_id=pic_id)

    json = {
            "type": "image/jpeg",
            "url": url,
            "author_name": "Source",
            "author_url": "https://www.pixiv.net/en/artworks/{post_id}".format(post_id=post_id),
        }

    return JSONResponse(content=json, media_type="application/json")

@router.get('/{post_id}')
@router.get('/{post_id}_p{pic_num}')
def embed(request: Request, post_id: int, pic_num: int | None = None):

    '''Assume post id is 8 digits long and pic num is 1 digits long.'''
    if pic_num:
        pic_id: str = str(post_id) + '_p' + str(pic_num)
    else:
        pic_id = str(post_id)

    '''Check if a user is accessing the embed from a discord client,
    if not (i.e. directly from a browser) then redirect to the .jpg version.'''
    if request.headers.get('user-agent') not in discord_useragent:
        return RedirectResponse(url='https://honkai-pictures.ru/api/embed/{pic_id}.jpg'.format(pic_id=pic_id))

    html = '''
        <html>
            <head>
                <link type="application/json+oembed" href="https://honkai-pictures.ru/api/embed/{pic_id}.json"/>
                <meta name="twitter:card" content="summary_large_image">
                <meta name="twitter:image" content="https://honkai-pictures.ru/api/embed/{pic_id}.jpg">
            </head>4
        </html>
    '''.format(pic_id=pic_id)

    return HTMLResponse(content=html)