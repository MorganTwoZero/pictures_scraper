from datetime import datetime, timedelta

from db.schemas import PostScheme
from settings import settings
from utils.crud.posts import save_to_db


TIMEZONE = settings.TIMEZONE

POST_LINK_TEMPLATE = 'https://bbs.mihoyo.com/bh3/article/'
POST_PREVIEW_TEMPLATE = '?x-oss-process=image/resize,s_500/quality,q_80/auto-orient,0/interlace,1/format,jpg'
AUTHOR_LINK_TEMPLATE = 'https://bbs.mihoyo.com/bh3/accountCenter/postList?id='


def mihoyo_bbs_save(db, posts):
    if posts:

        for post in posts:
            save_to_db(PostScheme(
                post_link=f"{POST_LINK_TEMPLATE + str(post['post']['post_id'])}",
                preview_link=f"{post['post']['cover'] + POST_PREVIEW_TEMPLATE}",              
                created=datetime.utcfromtimestamp(post['post']['created_at']
                ) + timedelta(hours=TIMEZONE),
                images_number=len(post['post']['images']),
                author=post['user']['nickname'],
                author_link=f"{AUTHOR_LINK_TEMPLATE + str(post['user']['uid'])}",
                author_profile_image=post['user']['avatar_url'],
                honkai=True,
                    ),
                db)