from datetime import datetime, timedelta
import logging
from typing import cast

from db.schemas import PostScheme
from settings import settings
from utils.crud.posts import save_to_db


#Logging
logger = logging.getLogger(__name__)

TIMEZONE = settings.TIMEZONE

POST_LINK_TEMPLATE = 'https://bcy.net/item/detail/'
AUTHOR_LINK_TEMPLATE = 'https://bcy.net/u/'

def parse(db, posts):
    if posts:

        for post in posts:
            post = cast("dict[str, str]", post['item_detail'])
            save_to_db(PostScheme(
                post_link=f"{POST_LINK_TEMPLATE + str(post['item_id'])}",
                preview_link=post['cover'],              
                created=datetime.utcfromtimestamp(int(post['ctime'])
                ) + timedelta(hours=TIMEZONE),
                images_number=int(post.get('pic_num', 1)),
                author=post['uname'],
                author_link=f"{AUTHOR_LINK_TEMPLATE + str(post['uid'])}",
                author_profile_image=post['avatar'],
                    ),
                db)
        logger.debug('Bcy updated')