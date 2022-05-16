from datetime import timedelta, datetime
from typing import Generator

from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_utils.tasks import repeat_every
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from db.database import SessionLocal, engine, Base
from db.schemas import PostCreate, Token, User, UserIn
from exceptions import credentials_exception
from scrapers.scrapers import *
from security import create_access_token, verify_password, verify_token
from settings import settings
from utils.crud import users
from utils.crud.posts import get_posts


Base.metadata.create_all(bind=engine) # type: ignore

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

app = FastAPI()

client = TestClient(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL,
        ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def update(db):
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

# Dependency
def get_db() -> Generator[Session, None, None]:
    try:
        db: Session = SessionLocal()
        yield db
    finally:
        db.close()  # type: ignore

@app.on_event("startup")
@repeat_every(seconds=60 * settings.UPDATE_TIMEOUT)
def test_update():
    '''
    Ugly hack to update on startup and timeout
    because of the way Depends() works
    '''
    client.get("/api/update")

# Routes
@app.get("/api/update")
def start_update(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    background_tasks.add_task(update, db)
    return {'message': 'Update started'}

@app.get("/api/{route}", response_model=list[PostCreate])
def api_posts(
    db: Session = Depends(get_db), 
    route: str | None = None, 
    page: int = 1, 
    offset: int = 20
        ):

    posts = get_posts(db, page, offset, route)
    return posts

@app.post('/api/register')
def register(user: UserIn, db: Session = Depends(get_db)):

    if users.create_user(user, db) is None:
        raise HTTPException(status_code=400, detail="User already exists")

    return {"message": "User created successfully"}


@app.post("/api/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
        ):

    user = users.get_user_by_username(username=form_data.username, db=db)
    if not user:
        raise credentials_exception

    correct_password = verify_password(form_data.password, user)
    if not correct_password:
        raise credentials_exception

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/users/me/", response_model=User)
async def read_users_me(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
        ):

    username = verify_token(token)
    user = users.get_user_by_username(username, db)
    return user