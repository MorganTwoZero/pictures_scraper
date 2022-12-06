from datetime import datetime, timezone
from typing import Sequence
import logging

import httpx
from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session

from db.schemas import PostScheme, UserWithTwitter, UserInDB
import deps
import parsers
from utils import request, crud
import security


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/api',
    tags=["site"],
)
async def save_homeline(db):
    users = crud.users.get_twitter_users(db)
    posts =  await request.request_homeline(users)
    parsers.homeline.parse(db, posts)

async def save_honkai(db):
    posts = await request.request_honkai()
    parsers.twitter_honkai.parse(db, posts.twitter_honkai)        
    parsers.pixiv.parse(db, posts.pixiv)
    parsers.mihoyo_bbs.parse(db, posts.bbs_mihoyo)
    parsers.bcy.parse(db, posts.bcy)       
    parsers.lofter.parse(db, posts.lofter)

last_update = datetime.now(tz=timezone.utc)
async def update(db: Session):
    logger.debug('Update started')

    try:
        await save_homeline(db)
        await save_honkai(db)
        logger.debug('Update ended')
    except httpx.TimeoutException:
        pass

@router.get("/update")
async def start_update(db: Session = Depends(deps.get_db)):
    await update(db)
    global last_update
    last_update = datetime.now(tz=timezone.utc)
    return {'message': 'Updated'}

@router.get('/update/last_update')
async def update_time() -> datetime:
    return last_update

@router.get("/honkai", response_model=Sequence[PostScheme])
def honkai_posts(
        request: Request,
        db: Session = Depends(deps.get_db),
        page: int = 1, 
        offset: int = 20
    ):

    logger.debug(f'Honkai posts requested, URL: {request.url}')
    posts = crud.posts.get_posts(db, page, offset)
    return posts

@router.get("/myfeed", response_model=Sequence[PostScheme])
async def homeline_posts(
        request: Request,
        db: Session = Depends(deps.get_db),
        page: int = 1, 
        offset: int = 20
    ):

    logger.debug(f'Myfeed requested, URL: {request.url}')

    user_in_db: UserInDB = security.get_current_user(request, db)
    user: UserWithTwitter = crud.users.get_user_with_twitter(user_in_db.username, db)
    
    if user.twitter_header:
        posts = crud.posts.my_feed_db_get(db, user, page, offset)
        return posts
    else:
        return 'Twitter header is not present'

@router.get("/like")
async def like(
    rqst: Request,
    post_link: str,
    db: Session = Depends(deps.get_db)
    ):

    logger.debug('Like requested, post link={}'.format(post_link))

    post_id: int = int(post_link[-20:-1])

    user_in_db: UserInDB = security.get_current_user(rqst, db)
    user: UserWithTwitter = crud.users.get_user_with_twitter(user_in_db.username, db)

    r: httpx.Response = await request.like_request(post_id, user)

    return {
        'status': r.status_code,
        'twitter_json': r.json()
        }

@router.get("/lofter")
async def lofter_link(lofter_link: str, preview: bool = False) -> Response:
    logger.debug('Lofter img requested, link={}'.format(lofter_link))

    main_pic_preview = "?imageView&thumbnail=500x0&quality=96"
    author_avatar_preview = "?imageView&thumbnail=60x60&quality=90&type=jpg"

    if preview:
        image = await request.lofter_proxy(lofter_link+main_pic_preview)
    else:
        image = await request.lofter_proxy(lofter_link+author_avatar_preview)
        
    return Response(content=image, media_type="image")