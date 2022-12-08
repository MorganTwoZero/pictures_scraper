from datetime import datetime, timedelta
import logging

from db.schemas import PostScheme
from settings import settings


logger = logging.getLogger(__name__)

SCARY_TAGS = settings.SCARY_TAGS.split()
SCARY_AUTHORS = settings.SCARY_AUTHORS.split()
POST_LINK_TEMPLATE = 'https://www.pixiv.net/en/artworks/'
AUTHOR_LINK_TEMPLATE = 'https://www.pixiv.net/en/users/'

def parse(posts):
    if posts:
        parsed = []

        for post in posts:

            scary_tag = any(tag in post['tags'] for tag in SCARY_TAGS)
            scary_author = post['author_details']['user_name'] in SCARY_AUTHORS

            if not scary_tag and not scary_author:
                parsed.append(
                    PostScheme(
                        post_link=f"{POST_LINK_TEMPLATE + post['id']}",
                        preview_link=post['url'],
                        images_number=post['page_count'],                    
                        created=datetime.utcfromtimestamp(
                            int(post['upload_timestamp'])
                        ) + timedelta(hours=settings.TIMEZONE),
                        author=post['author_details']['user_name'],
                        author_link=f"{AUTHOR_LINK_TEMPLATE + str(post['author_details']['user_id'])}",
                    )
                )
                    
        logger.debug('Pixiv updated')
        return parsed