from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.schemas import PostScheme
from dependency import get_db
from parsers.imports import *
from parsers.homeline_many_users import homeline_save_many_users
from utils.crud.posts import get_posts
from utils.request import request

router = APIRouter(
    prefix='/api',
    tags=["site"],
)

update_pending: bool = False
async def update(db):
    global update_pending
    update_pending = True
    print('Start update ' + str(datetime.now()))
    posts = await request()
    homeline_save(db, posts.twitter_homeline)
    print('Homeline updated')
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
    update_pending = False

@router.get("/update")
async def start_update(db: Session = Depends(get_db)):
    global update_pending
    if update_pending == True:
        return {"message": "Update already in progress"}
    await update(db)
    return {'message': 'Updated'}

@router.get("/honkai", response_model=list[PostScheme])
def honkai_posts(
    db: Session = Depends(get_db), 
    route = 'honkai', 
    page: int = 1, 
    offset: int = 20
    ):

    posts = get_posts(db, page, offset, route)
    return posts

@router.get("/homeline", response_model=list[PostScheme])
def homeline_posts(
    db: Session = Depends(get_db), 
    route = 'homeline', 
    page: int = 1, 
    offset: int = 20
    ):

    posts = get_posts(db, page, offset, route)
    return posts