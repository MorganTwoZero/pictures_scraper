import os
import inspect
from dotenv import load_dotenv
dotenv_path = os.path.dirname(__file__) + '/../.env'
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
from datetime import datetime

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_utils.tasks import repeat_every
from sqlalchemy.orm import Session

from backend.db import models, read_create
from backend.db.database import SessionLocal, engine
from backend.scrapers.lofter import lofter_save
from backend.scrapers.mihoyo_bbs import mihoyo_bbs_save
from backend.scrapers.pixiv import pixiv_save
from backend.scrapers.twitter import twitter_save
from backend.scrapers.twitter_homeline import homeline_save


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

app.mount("/static", StaticFiles(directory="backend/static"), name="static")

templates = Jinja2Templates(directory="backend/static/templates")

@app.on_event("startup")
@repeat_every(seconds=60 * UPDATE_TIMEOUT)
def update():    
    print(datetime.now())
    print('Updating...')
    homeline_save()
    print('Homeline updated.')
    twitter_save()
    print('Twitter updated.')
    pixiv_save()
    print('Pixiv updated.')
    mihoyo_bbs_save()
    print('Mihoyo updated.')
    lofter_save()
    print('Lofter updated.')
    print(datetime.now())


@app.get("/", response_class=HTMLResponse)
@app.get("/{page}", response_class=HTMLResponse)
def index(
    request: Request, 
    db: Session = Depends(get_db), 
    page: int | None = 1,
    offset: int = 20,
    ):
    posts = read_create.get_posts(db, page, offset)
    return templates.TemplateResponse(
        "stream.html", 
        {"request": request, "posts": posts, "page": page, "url": inspect.stack()[0][3]}
        )

@app.get("/homeline/", response_class=HTMLResponse)
@app.get("/homeline/{page}", response_class=HTMLResponse)
def homeline(
    request: Request, 
    db: Session = Depends(get_db), 
    page: int | None = 1,
    offset: int = 10,
    ):
    homeline_save()
    posts = read_create.get_homeline(db, page, offset)
    return templates.TemplateResponse(
        "stream.html", 
        {"request": request, "posts": posts, "page": page, "url": inspect.stack()[0][3]}
        )

@app.get("/api/")
def api(db: Session = Depends(get_db), page: int = 1, offset: int = 20):
    posts = read_create.get_posts(db, page, offset)
    return posts