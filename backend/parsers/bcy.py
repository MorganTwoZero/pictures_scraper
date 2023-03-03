from datetime import datetime, timedelta
import logging
from typing import cast

from db.schemas import PostScheme
from settings import settings


logger = logging.getLogger(__name__)

SCARY_AUTHORS = settings.SCARY_AUTHORS.split()
POST_LINK_TEMPLATE = 'https://bcy.net/item/detail/'
AUTHOR_LINK_TEMPLATE = 'https://bcy.net/u/'

def parse(posts):
    if posts:
        parsed = []

        for post in posts:
            post = cast("dict[str, str]", post['item_detail'])
            if post.get('cover') is not None and post['uname'] not in SCARY_AUTHORS:
            
                parsed.append(
                    PostScheme(
                        post_link=f"{POST_LINK_TEMPLATE + str(post['item_id'])}",
                        preview_link=post['cover'],              
                        created=datetime.utcfromtimestamp(
                            int(post['ctime'])
                        ) + timedelta(hours=settings.TIMEZONE),
                        images_number=int(post.get('pic_num', 1)),
                        author=post['uname'],
                        author_link=f"{AUTHOR_LINK_TEMPLATE + str(post['uid'])}",
                        author_profile_image=post['avatar'],
                    )
                )

        logger.debug('Bcy updated')
        return parsed