from datetime import datetime, timezone
from typing import Sequence
import logging

from fastapi import APIRouter, Depends, Request, Response
from httpx import AsyncClient
from sqlalchemy.orm import Session

from db.schemas import PostScheme
from db.models import HonkaiPost, TwitterFeedPost
import deps
import services
from utils import request, crud


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/api',
    tags=["site"],
)

last_update = datetime.now(tz=timezone.utc)

@router.get("/update")
async def start_update(db: Session = Depends(deps.get_db), client: AsyncClient = Depends(deps.get_request_client)):
    await services.update(db, client)
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
    posts = crud.posts.get_posts(db, page, offset, HonkaiPost)
    return posts

@router.get("/myfeed")
async def homeline_posts(
        request: Request,
        db: Session = Depends(deps.get_db),
        page: int = 1, 
        offset: int = 20
    ):
    logger.debug(f'Myfeed requested, URL: {request.url}')

    posts = crud.posts.get_posts(db, page, offset, TwitterFeedPost)
    return posts

@router.get("/like")
async def like(
    post_link: str,
    client: AsyncClient = Depends(deps.get_request_client)
    ):
    logger.debug('Like requested, post link={}'.format(post_link))

    post_id: int = int(post_link[-20:-1])
    r = await request.like_request(post_id, client)
    return {
        'status': r.status_code,
        'twitter_json': r.json()
        }

@router.get("/lofter")
async def lofter_link(lofter_link: str, preview: bool = False, client: AsyncClient = Depends(deps.get_request_client)) -> Response:
    logger.debug('Lofter img requested, link={}'.format(lofter_link))

    main_pic_preview = "?imageView&thumbnail=500x0&quality=96"
    author_avatar_preview = "?imageView&thumbnail=60x60&quality=90&type=jpg"

    client.headers = dict()
    if preview:
        image = await request.make_request(client, lofter_link+main_pic_preview)
    else:
        image = await request.make_request(client, lofter_link+author_avatar_preview)
        
    if image is None:
        return Response("Failed to load the image", 500)
    return Response(content=image.content, media_type="image")
