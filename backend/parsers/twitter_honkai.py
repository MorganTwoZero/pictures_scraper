from datetime import datetime, timedelta
from re import sub
import logging

from db.schemas import PostScheme
from settings import settings


logger = logging.getLogger(__name__)

def parse(posts):
    if posts:
        parsed = []

        for item in posts:
            if 'media' in item.get('entities'):

                parsed.append(
                    PostScheme(
                        #-7 due to 'photo/1' in link
                        post_link=item['entities']['media'][0]['expanded_url'][:-7],
                        preview_link=item['entities']['media'][0]['media_url_https'],
                        created=datetime.strptime(
                            item['created_at'], '%a %b %d %H:%M:%S %z %Y'
                            ) + timedelta(hours=settings.TIMEZONE),
                        images_number=len(item['entities']['media']),
                        author_link=sub(r'/status/.*', '', 
                            item['entities']['media'][0]['expanded_url']),
                        #not a "user@screen_name" because of api's data
                        author=sub(r'/status/.*', '', 
                            item['entities']['media'][0]['expanded_url'])[20:],
                        author_profile_image=None,
                    )
                )

        logger.debug('Twitter updated')
        return parsed