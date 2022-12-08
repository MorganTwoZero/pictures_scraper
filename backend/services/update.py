import logging

import httpx
from sqlalchemy.orm import Session

from utils import request, crud
import parsers


logger = logging.getLogger(__name__)

async def save_homeline(db):
    users = crud.users.get_twitter_users(db)
    try:
        feeds = await request.request_homeline(users)    
    except (httpx.TimeoutException, httpx.ConnectError):
        return

    for user, feed in feeds:
        if feed.is_success:
            parsed = parsers.homeline.parse(feed.json())
            for post in parsed:
                crud.posts.save_post_many_users(db, post, user)
    logger.debug('Homeline updated')

async def save_honkai(db):
    try:
        posts = await request.request_honkai()    
    except (httpx.TimeoutException, httpx.ConnectError):
        return

    parsed = [
        parsers.twitter_honkai.parse(posts.twitter_honkai),
        parsers.pixiv.parse(posts.pixiv),
        parsers.mihoyo_bbs.parse(posts.bbs_mihoyo),
        parsers.bcy.parse(posts.bcy),
        parsers.lofter.parse(posts.lofter),
    ]
    parsed = [item for sublist in parsed for item in sublist]

    for i in parsed:
        crud.posts.save_to_db(i, db)

async def update(db: Session):
    logger.debug('Update started')
    await save_homeline(db)
    await save_honkai(db)
    logger.debug('Update ended')