from datetime import datetime, timedelta

from db.schemas import PostScheme
from settings import settings
from utils.crud.posts import save_to_db


TIMEZONE = settings.TIMEZONE

SCARY_TAGS = settings.SCARY_TAGS.split()
SCARY_AUTHORS = settings.SCARY_AUTHORS.split()
POST_LINK_TEMPLATE = 'https://www.pixiv.net/en/artworks/'
AUTHOR_LINK_TEMPLATE = 'https://www.pixiv.net/en/users/'


def pixiv_save(db, posts):
    if posts:      

        for post in posts:
            scary_tag = any(tag in post['tags'] for tag in SCARY_TAGS)
            scary_author = post['author_details']['user_name'] in SCARY_AUTHORS
            if not scary_tag and not scary_author:
                save_to_db(PostScheme(
                    post_link=f"{POST_LINK_TEMPLATE + post['id']}",
                    preview_link=post['url'],
                    images_number=post['page_count'],                    
                    created=datetime.utcfromtimestamp(int(post['upload_timestamp'])
                    ) + timedelta(hours=TIMEZONE),
                    author=post['author_details']['user_name'],
                    author_link=f"{AUTHOR_LINK_TEMPLATE + str(post['author_details']['user_id'])}",
                    ),
                db)