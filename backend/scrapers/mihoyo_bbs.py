import os
from datetime import datetime, timedelta

import requests
from db.read_create import save_to_db
from db.schemas import PostCreate

TIMEZONE = int(os.environ['TIMEZONE'])

SEARCH_URL = 'https://bbs-api.mihoyo.com/post/wapi/getForumPostList?forum_id=4&gids=1&is_good=false&is_hot=false&page_size=20&sort_type=2'
POST_LINK_TEMPLATE = 'https://bbs.mihoyo.com/bh3/article/'
POST_PREVIEW_TEMPLATE = '?x-oss-process=image/resize,s_500/quality,q_80/auto-orient,0/interlace,1/format,jpg'
AUTHOR_LINK_TEMPLATE = 'https://bbs.mihoyo.com/bh3/accountCenter/postList?id='


def mihoyo_bbs_save():
    try:
        result = requests.get(url=SEARCH_URL).json()['data']['list']

        for post in result:
            save_to_db(PostCreate(
                post_link=f"{POST_LINK_TEMPLATE + str(post['post']['post_id'])}",
                preview_link=f"{post['post']['cover'] + POST_PREVIEW_TEMPLATE}",              
                created=datetime.utcfromtimestamp(post['post']['created_at']) + timedelta(hours=TIMEZONE),
                images_number=len(post['post']['images']),
                author=post['user']['nickname'],
                author_link=f"{AUTHOR_LINK_TEMPLATE + str(post['user']['uid'])}",
                author_profile_image=post['user']['avatar_url'],
                source='mihoyo_bbs',
                    )
                )
    except Exception:
        print('Failed to get https://bbs-api.mihoyo.com')
