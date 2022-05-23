import requests
import ast

from settings import settings


def get_image(link: str):
    PIXIV_HEADER: dict = ast.literal_eval(settings.PIXIV_HEADER)
    PIXIV_HEADER.update({'Referer': 'https://www.pixiv.net/'})
    img = requests.get(
        url=link,
        headers=PIXIV_HEADER
    ).content
    return img