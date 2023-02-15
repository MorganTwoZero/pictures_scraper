import re

from aiocache import cached

from utils.request import pixiv_proxy


@cached()
async def pixiv_proxy_image(post_id: int, pic_num: int) -> bytes | None:    
    url = 'https://www.pixiv.net/touch/ajax/illust/details?illust_id=' + str(post_id)
    
    json = await pixiv_proxy(url)
    if json is None:
        return
    post = json.json().get('body')
    if 'illust_details' not in post:
        return

    img_url = get_img_url(post.get('illust_details'), pic_num)    
    img = await pixiv_proxy(img_url)        
    return img.content

def get_img_url(json: dict, pic_num: int) -> str:
    if pic_num == 0:
        img_url = json['url']
    else:
        img_url = json['manga_a'][pic_num]['url']        
    img_url = re.sub(r'.*/img-master', 'https://i.pximg.net/img-master', img_url)

    return img_url