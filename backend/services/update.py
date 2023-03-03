import logging

import httpx
from sqlalchemy.orm import Session

from db.models import HonkaiPost, TwitterFeedPost
from utils import request, crud
import parsers


logger = logging.getLogger(__name__)

async def save_posts(db, client: httpx.AsyncClient):
    try:
        posts = await request.request_honkai(client)    
    except (httpx.TimeoutException, httpx.ConnectError):
        return

    myfeed = parsers.homeline.parse(posts.myfeed)
    for post in myfeed:
                crud.posts.save_post(post, db, TwitterFeedPost)

    parsed = [
        parsers.twitter_honkai.parse(posts.twitter_honkai),
        parsers.pixiv.parse(posts.pixiv),
        parsers.mihoyo_bbs.parse(posts.bbs_mihoyo),
        parsers.bcy.parse(posts.bcy),
        parsers.lofter.parse(posts.lofter),
    ]
    parsed = [item for sublist in parsed for item in sublist]

    for post in parsed:
        crud.posts.save_post(post, db, HonkaiPost)

async def update(db: Session, client: httpx.AsyncClient):
    logger.debug('Update started')
    await save_posts(db, client)
    logger.debug('Update ended')