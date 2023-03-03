import re

from aiocache import cached
from httpx import AsyncClient, Response

from utils.request import make_request


@cached()
async def pixiv_proxy_image(post_id: int, pic_num: int, client: AsyncClient) -> Response | None:    
    url = 'https://www.pixiv.net/touch/ajax/illust/details?illust_id=' + str(post_id)
    
    json = await make_request(client, url)
    if json is None:
        return
    post = json.json().get('body')
    if 'illust_details' not in post:
        return

    img_url = get_img_url(post.get('illust_details'), pic_num)    
    img = await make_request(client, img_url)
    return img

def get_img_url(json: dict, pic_num: int) -> str:
    if pic_num == 0:
        img_url = json['url']
    else:
        img_url = json['manga_a'][pic_num]['url']        
    img_url = re.sub(r'.*/img-master', 'https://i.pximg.net/img-master', img_url)

    return img_url