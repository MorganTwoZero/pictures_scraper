import os

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every
from sqlalchemy.orm import Session

from db import models, read_create
from db.database import SessionLocal, engine
from scrapers.lofter import lofter_save
from scrapers.mihoyo_bbs import mihoyo_bbs_save
from scrapers.pixiv import pixiv_save
from scrapers.twitter import twitter_save
from scrapers.twitter_homeline import homeline_save


UPDATE_TIMEOUT = int(os.environ['UPDATE_TIMEOUT'])

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
@repeat_every(seconds=60 * UPDATE_TIMEOUT)
def update():
    homeline_save()
    twitter_save()
    pixiv_save()
    mihoyo_bbs_save()
    lofter_save()
    
@app.get("/api/{route}")
def api_posts(route: str, db: Session = Depends(get_db), page: int = 1, offset: int = 20):
    if route == 'homeline':
        homeline_save()
    posts = read_create.get_posts(db, page, offset, route=route)
    return posts