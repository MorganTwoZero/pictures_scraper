from datetime import datetime, timedelta
from typing import Iterable

from httpx import Response

from db.schemas import PostScheme, UserWithTwitter
from settings import settings
from utils.crud.posts import save_post_many_users


TIMEZONE = settings.TIMEZONE


def homeline_save_many_users(
    db, 
    result_and_user: Iterable[tuple[UserWithTwitter, Response]],
    ):
    for i in result_and_user:
        user, response = i
        assert response.json()

        for post in response.json():
            if 'media' in post['entities']:
                post = PostScheme(
                    # -7 due to 'photo/1' in link
                    post_link=post['entities']['media'][0]['expanded_url'][:-7],
                    preview_link=post['entities']['media'][0]['media_url_https'],
                    created=datetime.strptime(
                        post['created_at'], '%a %b %d %H:%M:%S %z %Y'
                    ) + timedelta(hours=TIMEZONE),
                    images_number=len(post['entities']['media']),
                    author=f'{post["user"]["name"]}@{post["user"]["screen_name"]}',
                    author_link=f'https://twitter.com/{post["user"]["screen_name"]}',
                    author_profile_image=post['user']['profile_image_url_https'],
                )
                save_post_many_users(db, post, user)