from datetime import datetime, timedelta

from httpx import Response

from db.schemas import TwitterPostScheme, UserWithTwitter
from settings import settings
from utils.crud.posts import save_to_db_many_users


TIMEZONE = settings.TIMEZONE


def homeline_save_many_users(db, result_and_user: list[tuple[UserWithTwitter, Response]]):
    for i in result_and_user:
        user, response = i
        assert response.json()

        for item in response.json():
            if 'media' in item['entities']:
                post = TwitterPostScheme(
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
                )
                save_to_db_many_users(db, post, user)