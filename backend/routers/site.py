from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.schemas import PostScheme
from dependency import get_db
from scrapers.imports import *
from utils.crud.posts import get_posts
from utils.request import request

router = APIRouter(
    prefix='/api',
    tags=["site"],
)

async def update(db):
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

@router.get("/update")
async def start_update(db: Session = Depends(get_db)):
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