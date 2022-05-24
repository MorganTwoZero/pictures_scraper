from datetime import datetime
from typing import Literal

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.schemas import PostScheme
from dependency import get_db
from scrapers.imports import *
from utils.crud.posts import get_posts

router = APIRouter(
    prefix='/api',
    tags=["site"],
)

update_pending: bool = False
def update(db):
    global update_pending
    update_pending = True
    print('Start update ' + str(datetime.now()))
    homeline_save(db)
    print('Homeline updated')
    twitter_save(db)
    print('Twitter updated')
    pixiv_save(db)
    print('Pixiv updated')
    mihoyo_bbs_save(db)
    print('Mihoyo updated')
    lofter_save(db)
    print('Lofter updated')
    print('End update ' + str(datetime.now()))
    update_pending = False

@router.get("/update")
def start_update(db: Session = Depends(get_db)):
    global update_pending
    if update_pending == True:
        return {"message": "Update already in progress"}
    update(db)
    return {'message': 'Updated'}

@router.get("/honkai", response_model=list[PostScheme])
def api_posts(
    db: Session = Depends(get_db), 
    route = 'honkai', 
    page: int = 1, 
    offset: int = 20
    ):

    posts = get_posts(db, page, offset, route)
    return posts

@router.get("/homeline", response_model=list[PostScheme])
def api_posts(
    db: Session = Depends(get_db), 
    route = 'homeline', 
    page: int = 1, 
    offset: int = 20
    ):

    posts = get_posts(db, page, offset, route)
    return posts