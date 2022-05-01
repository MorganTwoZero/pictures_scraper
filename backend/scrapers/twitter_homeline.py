import ast
import os
from datetime import datetime, timedelta

import requests
from backend.db.read_create import save_to_db
from backend.db.schemas import PostCreate

TWITTER_HOME_URL = os.environ['TWITTER_HOME_URL']
TIMEZONE = int(os.environ['TIMEZONE'])
TWITTER_HEADER = ast.literal_eval(os.environ['TWITTER_HEADER'])

def homeline_save():
    r = requests.get(url=TWITTER_HOME_URL, headers=TWITTER_HEADER).json()

    for item in r:
        if 'media' in item['entities']:
            save_to_db(PostCreate(
                post_link=item['entities']['media'][0]['expanded_url'][:-7], #-7 due to 'photo/1' in link
                preview_link=item['entities']['media'][0]['media_url_https'],
                created=datetime.strptime(item['created_at'], '%a %b %d %H:%M:%S %z %Y') + timedelta(hours=TIMEZONE),
                source='homeline',
                images_number=len(item['entities']['media']),
                author=f'{item["user"]["name"]}@{item["user"]["screen_name"]}',
                author_link=f'https://twitter.com/{item["user"]["screen_name"]}',
                author_profile_image=item['user']['profile_image_url_https'],
                    )
                )
