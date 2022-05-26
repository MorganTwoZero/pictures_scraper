import re

from fastapi import HTTPException

from utils.request import pixiv_proxy


async def pixiv_proxy_image(post_id: int, big: bool = True):
    url = 'https://www.pixiv.net/touch/ajax/illust/details?illust_id=' + str(post_id)
    post = await pixiv_proxy(url)
    assert post is not None
    post = post.json().get('body')
    if not 'illust_details' in post:
        raise HTTPException(status_code=404, detail="Post not found")
    post = post.get('illust_details')
    if big:
        if post.get('url_big'):
            img_url = post['url_big']
        else:
            img_url = post['manga_a'][0]['url_big']
    else:
        img_url = re.sub(r'.*/img-master', 'https://i.pximg.net/img-master', post['url'])
    img = await pixiv_proxy(img_url)
    assert img is not None
    img = img.content
    return img