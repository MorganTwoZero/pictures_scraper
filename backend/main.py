from datetime import timedelta, datetime
from typing import Generator, Literal

from fastapi import Body, Depends, FastAPI, HTTPException, Response, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_utils.tasks import repeat_every
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from db.database import SessionLocal, engine, Base
from db.schemas import PostScheme, UserOut, UserFront
from exceptions import credentials_exception
from scrapers.scrapers import *
from security import create_access_token, verify_password, verify_token
from settings import settings
from utils.crud import users
from utils.crud.posts import get_posts
from utils.image import get_image, get_image_big, embed



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
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
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
#Users
@app.post('/api/register')
def register(user: UserFront, db: Session = Depends(get_db)):

    if users.create_user(user, db) is None:
        raise HTTPException(status_code=400, detail="User already exists")

    return {"message": "User created successfully"}


@app.post("/api/login")
async def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
        ):
        
    user = users.get_user_by_username(username=form_data.username, db=db)
    if not user:
        raise credentials_exception

    correct_password = verify_password(form_data.password, user)
    if not correct_password:
        raise credentials_exception

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token: str = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires)

    response.set_cookie(
        key="Authorization", 
        value=access_token, 
        httponly=True, 
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60, 
        samesite='Strict',
        secure=True,
        ) 

    return {'message': 'Authenticated'}

@app.get("/api/logout")
async def logout(response: Response):
    response.set_cookie(
        key="Authorization", 
        value="", 
        httponly=True, 
        max_age=0, 
        samesite='Strict',
        secure=True,
        ) 
    return {'message': 'Logged out'}

@app.get("/api/user", response_model=UserOut)
async def read_users_me(
    request: Request,
    db: Session = Depends(get_db)
        ):

    token = request.cookies.get('Authorization')

    username = verify_token(token)
    if not username:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = users.get_user_by_username(username, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

#Content
@app.get("/api/update")
def start_update(db: Session = Depends(get_db)):
    global update_pending
    if update_pending == True:
        return {"message": "Update already in progress"}
    update(db)
    return {'message': 'Updated'}

@app.post('/api/get_image', response_class=Response)
def load_image(link: str = Body(default=None)):
    image = get_image(link)
    return Response(content=image, media_type="image")

@app.get('/api/get_image/big', response_class=Response)
def load_image_big(post_id: int):
    image = get_image_big(post_id)
    return Response(content=image, media_type="image")

@app.get('/api/embed/{post_id}.jpg', response_class=Response)
def get_embed_img(post_id: int):
    image = embed(post_id)
    if image is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return Response(content=image, media_type="image")

@app.get('/api/embed/{post_id}', response_class=HTMLResponse)
def get_embed(post_id: int):
    html_content = """
        <html>
            <head>
                <meta property="og:title" content="Source" />
                 <meta property="og:url" content="https://www.pixiv.net/en/artworks/{}" />
                <meta property="og:image" content="https://honkai-pictures.ru/api/embed/{}.jpg"/>

                <!-- Include this to make the og:image larger -->
                <meta name="twitter:card" content="summary_large_image">
            </head>
            <body>
                <h1>Look ma! HTML!</h1>
            </body>
        </html>
        """.format(post_id, post_id)
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/api/{route}", response_model=list[PostScheme])
def api_posts(
    db: Session = Depends(get_db), 
    route: Literal['honkai', 'homeline'] = 'honkai', 
    page: int = 1, 
    offset: int = 20
        ):

    posts = get_posts(db, page, offset, route)
    return posts
