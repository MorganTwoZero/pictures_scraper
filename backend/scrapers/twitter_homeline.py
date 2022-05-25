from datetime import datetime, timedelta

from db.schemas import PostScheme
from settings import settings
from utils.crud.posts import save_to_db


TIMEZONE = settings.TIMEZONE

def homeline_save(db, r):
    try:
        for item in r.json():
            if 'media' in item['entities']:
                save_to_db(PostScheme(        
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
    except:
        print('Failed to get homeline')