from datetime import datetime, timedelta
from typing import Sequence
import logging

from httpx import Response
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from db.schemas import PostScheme, UserWithTwitter, UserInDB
from dependency import get_db
from parsers.imports import *
from utils.request import request_honkai, request_homeline, like_request
from utils.crud.users import get_all_users_with_twitter, get_user_with_twitter
from utils.crud.posts import get_posts, my_feed_db_get
from settings import settings
from security import get_current_user


#Logging
logger = logging.getLogger(__name__)

#Routers
router = APIRouter(
    prefix='/api',
    tags=["site"],
)

last_update = datetime.now() + timedelta(hours=settings.TIMEZONE)
async def update(db: Session):
    logger.info('Update started')

    try:
        users = get_all_users_with_twitter(db)
        posts =  await request_homeline(users)
        homeline_save_many_users(db, posts)
        logger.info('Homeline updated')

        posts = await request_honkai()
        twitter_save(db, posts.twitter_honkai)
        logger.info('Twitter updated')
        pixiv_save(db, posts.pixiv)
        logger.info('Pixiv updated')
        mihoyo_bbs_save(db, posts.bbs_mihoyo)
        logger.info('Mihoyo updated')
        for html in posts.lofter:
            lofter_save(db, html)
        logger.info('Lofter updated')
        logger.info('Update ended')
    except:
        logger.exception('error')

@router.get("/update")
async def start_update(db: Session = Depends(get_db)):
    await update(db)
    global last_update
    last_update = datetime.now() + timedelta(hours=settings.TIMEZONE)
    return {'message': 'Updated'}

@router.get('/update/last_update')
async def update_time():
    return last_update

@router.get("/honkai", response_model=Sequence[PostScheme])
def honkai_posts(
    request: Request,
    db: Session = Depends(get_db),
    page: int = 1, 
    offset: int = 5
    ):

    logger.debug(f'Honkai posts requested, URL: {request.url}')
    posts = get_posts(db, page, offset)
    return posts

@router.get("/myfeed", response_model=Sequence[PostScheme])
async def homeline_posts(
    request: Request,
    db: Session = Depends(get_db),
    page: int = 1, 
    offset: int = 5
    ):

    logger.debug(f'Myfeed requested, URL: {request.url}')

    user_in_db: UserInDB = get_current_user(request, db)
    user: UserWithTwitter = get_user_with_twitter(user_in_db.username, db)
    
    if user.twitter_header:
        posts = my_feed_db_get(db, user, page, offset)
        return posts
    else:
        return 'Twitter header is not present'

@router.get("/like")
async def like(
    request: Request,
    post_link: str,
    db: Session = Depends(get_db)
    ):

    logger.debug('Like requested, post link={}'.format(post_link))

    post_id: int = int(post_link[-20:-1])

    user_in_db: UserInDB = get_current_user(request, db)
    user: UserWithTwitter = get_user_with_twitter(user_in_db.username, db)

    r: Response = await like_request(post_id, user)

    return {
        'status': r.status_code,
        'twitter_json': r.json()
        }