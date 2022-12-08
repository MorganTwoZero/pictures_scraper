from datetime import datetime, timedelta
import logging

from db.schemas import PostScheme
from settings import settings


logger = logging.getLogger(__name__)

POST_LINK_TEMPLATE = 'https://bbs.mihoyo.com/bh3/article/'
POST_PREVIEW_TEMPLATE = '?x-oss-process=image/resize,s_500/quality,q_80/auto-orient,0/interlace,1/format,jpg'
AUTHOR_LINK_TEMPLATE = 'https://bbs.mihoyo.com/bh3/accountCenter/postList?id='

def parse(posts):
    if posts:
        parsed = []

        for post in posts:
            parsed.append(
                PostScheme(
                post_link=f"{POST_LINK_TEMPLATE + str(post['post']['post_id'])}",
                preview_link=f"{post['post']['cover'] + POST_PREVIEW_TEMPLATE}",              
                created=datetime.utcfromtimestamp(
                    post['post']['created_at']
                ) + timedelta(hours=settings.TIMEZONE),
                images_number=len(post['post']['images']),
                author=post['user']['nickname'],
                author_link=f"{AUTHOR_LINK_TEMPLATE + str(post['user']['uid'])}",
                author_profile_image=post['user']['avatar_url'],
            )
        )
        logger.debug('Mihoyo updated')
        return parsed