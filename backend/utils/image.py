import requests
import ast

from settings import settings

PIXIV_HEADER: dict = ast.literal_eval(settings.PIXIV_HEADER)
PIXIV_HEADER.update({'Referer': 'https://www.pixiv.net/'})

def get_image(link: str):
    img = requests.get(
        url=link,
        headers=PIXIV_HEADER
    ).content
    return img

def get_image_big(post_id: int):
    url = 'https://www.pixiv.net/touch/ajax/illust/details?illust_id=' + str(post_id)
    post = requests.get(
        url=url,
        headers=PIXIV_HEADER
    ).json()['body']['illust_details']
    if post.get('url_big'):
        img_url = post['url_big']
    else:
        img_url = post['manga_a'][0]['url_big']
    img_url
    img = requests.get(img_url, headers=PIXIV_HEADER).content
    return img

def embed(post_id: int):
    url = 'https://www.pixiv.net/touch/ajax/illust/details?illust_id=' + str(post_id)
    post = requests.get(url, headers=PIXIV_HEADER).json()['body']['illust_details']
    img_url = post['url']
    img = requests.get(img_url, headers=PIXIV_HEADER).content
    return img