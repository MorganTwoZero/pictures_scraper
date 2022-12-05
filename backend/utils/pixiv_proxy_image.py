import re

from aiocache import cached
from fastapi import HTTPException

from utils.request import pixiv_proxy


@cached()
async def pixiv_proxy_image(post_id: int, pic_num: int, is_big: bool) -> bytes | None:
    
    url = 'https://www.pixiv.net/touch/ajax/illust/details?illust_id=' + str(post_id)
    
    post = await pixiv_proxy(url)
    if post is None:
        raise HTTPException(status_code=500, detail="Request error")

    post = post.json().get('body')
    if 'illust_details' not in post:
        return None
        
    post = post.get('illust_details')

    img_url = get_img_url(post, pic_num, is_big)
    
    img = await pixiv_proxy(img_url)
    if img is None:
        return None
        
    return img.content

def get_img_url(json: dict, pic_num: int, is_big: bool) -> str:

    if is_big:
        if pic_num == 0:
            img_url = json['url_big']
        else:
            img_url = json['manga_a'][pic_num]['url_big']
    else:
        if pic_num == 0:
            img_url = json['url']
        else:
            img_url = json['manga_a'][pic_num]['url']        
        img_url = re.sub(r'.*/img-master', 'https://i.pximg.net/img-master', img_url)

    return img_url