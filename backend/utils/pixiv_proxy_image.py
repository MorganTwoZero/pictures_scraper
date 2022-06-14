import re

from fastapi import HTTPException

from backend.utils.request import pixiv_proxy


async def pixiv_proxy_image(pic_id: str, big: bool):
    
    '''Check if requested image is the only image in the post.
    Get post id and pic num.'''
    if pic_id[-3:-1] == '_p':
        pixiv_id = pic_id[:-3]
        pic_num = int(pic_id[-1])
    else:
        pixiv_id = pic_id
        pic_num = int(0)
    
    url = 'https://www.pixiv.net/touch/ajax/illust/details?illust_id=' + pixiv_id
    
    post = await pixiv_proxy(url)
    if post is None:
        raise HTTPException(status_code=500, detail="Request error")
    post = post.json().get('body')
    if not 'illust_details' in post:
        raise HTTPException(status_code=404, detail="Post not found")
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
        raise HTTPException(status_code=404, detail="Image not found")
    img = img.content
    return img