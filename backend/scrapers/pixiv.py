import ast
import os
from datetime import datetime, timedelta

import requests
from backend.db.read_create import save_to_db
from backend.db.schemas import PostCreate

TIMEZONE = int(os.environ['TIMEZONE'])

PIXIV_URL = os.environ['PIXIV_URL']
SCARY_TAGS = os.environ['SCARY_TAGS'].split()
SCARY_AUTHORS = os.environ['SCARY_AUTHORS'].split()
PIXIV_HEADER = ast.literal_eval(os.environ['PIXIV_HEADER'])
POST_LINK_TEMPLATE = 'https://www.pixiv.net/en/artworks/'
AUTHOR_LINK_TEMPLATE = 'https://www.pixiv.net/en/users/'


def pixiv_save():
    result = requests.get(url=PIXIV_URL, headers=PIXIV_HEADER).json()['body']['illusts']
    for post in result:
        scary_tag = any(tag in post['tags'] for tag in SCARY_TAGS)
        scary_author = post['author_details']['user_name'] in SCARY_AUTHORS
        if not scary_tag and not scary_author:
            save_to_db(PostCreate(
                post_link=f"{POST_LINK_TEMPLATE + post['id']}",
                preview_link=post['url'],
                images_number=post['page_count'],                    
                created=datetime.utcfromtimestamp(int(post['upload_timestamp'])) + timedelta(hours=TIMEZONE),
                author=post['author_details']['user_name'],
                author_link=f"{AUTHOR_LINK_TEMPLATE + str(post['author_details']['user_id'])}",
                source='pixiv'
                )
            )
