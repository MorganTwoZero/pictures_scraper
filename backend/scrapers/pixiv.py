import ast
from datetime import datetime, timedelta

import requests

from db.schemas import PostScheme
from settings import settings
from utils.crud.posts import save_to_db


TIMEZONE = settings.TIMEZONE

PIXIV_URL = settings.PIXIV_URL
SCARY_TAGS = settings.SCARY_TAGS.split()
SCARY_AUTHORS = settings.SCARY_AUTHORS.split()
PIXIV_HEADER:dict = ast.literal_eval(settings.PIXIV_HEADER)
POST_LINK_TEMPLATE = 'https://www.pixiv.net/en/artworks/'
AUTHOR_LINK_TEMPLATE = 'https://www.pixiv.net/en/users/'


def pixiv_save(db):
    result = requests.get(url=PIXIV_URL, headers=PIXIV_HEADER).json()['body']['illusts']        

    for post in result:
        scary_tag = any(tag in post['tags'] for tag in SCARY_TAGS)
        scary_author = post['author_details']['user_name'] in SCARY_AUTHORS
        if not scary_tag and not scary_author:
            save_to_db(PostScheme(
                post_link=f"{POST_LINK_TEMPLATE + post['id']}",
                preview_link=post['url'],
                images_number=post['page_count'],                    
                created=datetime.utcfromtimestamp(int(post['upload_timestamp'])
                ) + timedelta(hours=TIMEZONE),
                author=post['author_details']['user_name'],
                author_link=f"{AUTHOR_LINK_TEMPLATE + str(post['author_details']['user_id'])}",
                honkai=True,
                ),
            db)
