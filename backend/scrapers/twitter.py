import ast
from datetime import datetime, timedelta
from re import sub

import requests

from db.schemas import PostScheme
from settings import settings
from utils.crud.posts import save_to_db

TIMEZONE = settings.TIMEZONE

TWITTER_SEARCH_URL = settings.TWITTER_SEARCH_URL
TWITTER_HEADER = ast.literal_eval(settings.TWITTER_HEADER)

def twitter_save(db):
    r = list(requests.get(
        url=TWITTER_SEARCH_URL,
        headers=TWITTER_HEADER,
        ).json()['globalObjects']['tweets'].values())

    for item in r:
        if 'media' in item['entities']:
            save_to_db(PostScheme(
                    #-7 due to 'photo/1' in link
                    post_link=item['entities']['media'][0]['expanded_url'][:-7],
                    preview_link=item['entities']['media'][0]['media_url_https'],
                    created=datetime.strptime(
                        item['created_at'], '%a %b %d %H:%M:%S %z %Y'
                        ) + timedelta(hours=TIMEZONE),
                    images_number=len(item['entities']['media']),
                    author_link=sub(r'/status/.*', '', 
                        item['entities']['media'][0]['expanded_url']),
                    #not a "user@screen_name" because of api's data
                    author=sub(r'/status/.*', '', 
                        item['entities']['media'][0]['expanded_url'])[20:],
                    author_profile_image=None,
                    honkai=True,
                    ),
                db)