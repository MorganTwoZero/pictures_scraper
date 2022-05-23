import requests
import ast

from fastapi import HTTPException

from settings import settings


PIXIV_HEADER: dict = ast.literal_eval(settings.PIXIV_HEADER)
PIXIV_HEADER.update({'Referer': 'https://www.pixiv.net/'})

def request_image(post_id: int, big: bool = False):
    url = 'https://www.pixiv.net/touch/ajax/illust/details?illust_id=' + str(post_id)
    post = requests.get(url, headers=PIXIV_HEADER).json().get('body')
    if not 'illust_details' in post:
        raise HTTPException(status_code=404, detail="Post not found")
    post = post.get('illust_details')
    if big:
        if post.get('url_big'):
            img_url = post['url_big']
        else:
            img_url = post['manga_a'][0]['url_big']
    else:
        img_url = post['url']
    img = requests.get(img_url, headers=PIXIV_HEADER).content
    return img