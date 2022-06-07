from datetime import datetime
from typing import Iterable, Sequence

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from db.schemas import PostScheme, TwitterPostScheme, UserWithTwitter, UserInDB
from dependency import get_db
from parsers.imports import *
from utils.crud.posts import get_posts, my_feed_db_get
from utils.request import request, request_homeline_many_users
from utils.crud.users import get_users_with_twitter_credentials, get_user_with_twitter
from security import get_current_user

router = APIRouter(
    prefix='/api',
    tags=["site"],
)

async def update(db: Session):
    print('Start update ' + str(datetime.now()))

    users = get_users_with_twitter_credentials(db)
    posts =  await request_homeline_many_users(users)
    homeline_save_many_users(db, posts)
    print('Homeline updated')

    posts = await request()
    twitter_save(db, posts.twitter_honkai)
    print('Twitter updated')
    pixiv_save(db, posts.pixiv)
    print('Pixiv updated')
    mihoyo_bbs_save(db, posts.bbs_mihoyo)
    print('Mihoyo updated')
    for html in posts.lofter:
        lofter_save(db, html)
    print('Lofter updated')
    print('End update ' + str(datetime.now()))

@router.get("/update")
async def start_update(db: Session = Depends(get_db)):
    await update(db)
    return {'message': 'Updated'}

@router.get("/honkai", response_model=Iterable[PostScheme])
def honkai_posts(
    db: Session = Depends(get_db),
    page: int = 1, 
    offset: int = 20
    ):

    posts = get_posts(db, page, offset)
    return posts

@router.get("/myfeed", response_model=Sequence[TwitterPostScheme])
async def homeline_posts(
    request: Request,
    db: Session = Depends(get_db),
    page: int = 1, 
    offset: int = 20
    ):

    user_in_db: UserInDB = get_current_user(request, db)
    user: UserWithTwitter = get_user_with_twitter(user_in_db.username, db)
    if user.twitter_header:
        posts = my_feed_db_get(db, user, page, offset)
        return posts