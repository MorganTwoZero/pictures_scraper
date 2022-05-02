import ast
import os
from datetime import datetime, timedelta
from re import sub

import requests
from db.read_create import save_to_db
from db.schemas import PostCreate

TWITTER_SEARCH_URL = os.environ['TWITTER_SEARCH_URL']
TIMEZONE = int(os.environ['TIMEZONE'])
TWITTER_HEADER = ast.literal_eval(os.environ['TWITTER_HEADER'])

def twitter_save():
    r = list(requests.get(
        url=TWITTER_SEARCH_URL,
        headers=TWITTER_HEADER,
        ).json()['globalObjects']['tweets'].values())

    for item in r:
        if 'media' in item['entities']:
            save_to_db(PostCreate(
                post_link=item['entities']['media'][0]['expanded_url'][:-7], #-7 due to 'photo/1' in link
                preview_link=item['entities']['media'][0]['media_url_https'],
                created=datetime.strptime(item['created_at'], '%a %b %d %H:%M:%S %z %Y') + timedelta(hours=TIMEZONE),
                source='twitter',
                images_number=len(item['entities']['media']),
                author_link=sub(r'/status/.*', '', item['entities']['media'][0]['expanded_url']),
                author=sub(r'/status/.*', '', item['entities']['media'][0]['expanded_url'])[20:],
                    )
                )