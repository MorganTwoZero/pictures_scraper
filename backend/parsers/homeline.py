from datetime import datetime, timedelta
from typing import Iterable

from db.schemas import PostScheme
from settings import settings


def parse(feed: Iterable) -> Iterable[PostScheme]:
    parsed = []
    for post in feed:
        if 'media' in post.get('entities'):

            parsed.append(
                PostScheme(
                    # -7 due to 'photo/1' in link
                    post_link=post['entities']['media'][0]['expanded_url'][:-7],
                    preview_link=post['entities']['media'][0]['media_url_https'],
                    created=datetime.strptime(
                        post['created_at'], '%a %b %d %H:%M:%S %z %Y'
                    ) + timedelta(hours=settings.TIMEZONE),
                    images_number=len(post['entities']['media']),
                    author=f'{post["user"]["name"]}@{post["user"]["screen_name"]}',
                    author_link=f'https://twitter.com/{post["user"]["screen_name"]}',
                    author_profile_image=post['user']['profile_image_url_https'],
                )
            )

    return parsed