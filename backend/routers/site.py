from datetime import datetime, timezone
from typing import Sequence
import logging

from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session

from db.schemas import PostScheme, UserInDB
import deps
import services
from utils import request, crud
import security


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/api',
    tags=["site"],
)

last_update = datetime.now(tz=timezone.utc)

@router.get("/update")
async def start_update(db: Session = Depends(deps.get_db)):
    await services.update(db)
    set_update_time()
    return {'message': 'Updated'}

def set_update_time():
    global last_update
    last_update = datetime.now(tz=timezone.utc)

@router.get('/update/last_update')
async def last_update_time() -> datetime:
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

@router.get("/myfeed")
async def homeline_posts(
        request: Request,
        db: Session = Depends(deps.get_db),
        page: int = 1, 
        offset: int = 20
    ):

    logger.debug(f'Myfeed requested, URL: {request.url}')

    user_in_db: UserInDB = security.get_current_user(request, db)
    user = crud.users.get_user_with_twitter(user_in_db.username, db)
    
    if user:
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
    user = crud.users.get_user_with_twitter(user_in_db.username, db)

    if user:
        r = await request.like_request(post_id, user)

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