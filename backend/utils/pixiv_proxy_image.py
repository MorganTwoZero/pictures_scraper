import re
import logging

from fastapi import HTTPException

from utils.request import pixiv_proxy


async def pixiv_proxy_image(post_id: int, pic_num: int, big: bool) -> bytes | None:
    
    url = 'https://www.pixiv.net/touch/ajax/illust/details?illust_id=' + str(post_id)
    
    post = await pixiv_proxy(url)
    if post is None:
        raise HTTPException(status_code=500, detail="Request error")
    post = post.json().get('body')
    if not 'illust_details' in post:
        return None
    post = post.get('illust_details')

    if big:
        if pic_num == 0:
            img_url = post['url_big']
        else:
            img_url = post['manga_a'][pic_num]['url_big']
    else:
        if pic_num == 0:
            img_url = post['url']
        else:
            img_url = post['manga_a'][pic_num]['url']        
        img_url = re.sub(r'.*/img-master', 'https://i.pximg.net/img-master', img_url)
    
    img = await pixiv_proxy(img_url)
    if img is None:
        return None
    img = img.content
    return img