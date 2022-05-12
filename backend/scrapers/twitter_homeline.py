import ast
from datetime import datetime, timedelta

import requests

from db.schemas import PostCreate
from settings import settings
from utils.crud.posts import save_to_db

TIMEZONE = settings.TIMEZONE

TWITTER_HOME_URL = settings.TWITTER_HOME_URL
TWITTER_HEADER = ast.literal_eval(settings.TWITTER_HEADER)


def homeline_save(db):
    r = requests.get(url=TWITTER_HOME_URL, headers=TWITTER_HEADER).json()
    for item in r:
        if 'media' in item['entities']:
            save_to_db(PostCreate(        
                # -7 due to 'photo/1' in link        
                post_link=item['entities']['media'][0]['expanded_url'][:-7],
                preview_link=item['entities']['media'][0]['media_url_https'],
                created=datetime.strptime(
                    item['created_at'], '%a %b %d %H:%M:%S %z %Y'
                    ) + timedelta(hours=TIMEZONE),
                images_number=len(item['entities']['media']),
                author=f'{item["user"]["name"]}@{item["user"]["screen_name"]}',
                author_link=f'https://twitter.com/{item["user"]["screen_name"]}',
                author_profile_image=item['user']['profile_image_url_https'],
                honkai=False
                ),
            db)
