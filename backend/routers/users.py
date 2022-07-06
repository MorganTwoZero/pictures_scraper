from datetime import timedelta

from fastapi import APIRouter, Depends, Form, \
    HTTPException, Response, Request
from sqlalchemy.orm import Session

from db.schemas import UserFront, Settings as SettingsScheme
from dependency import get_db
from exceptions import credentials_exception
from security import create_access_token, \
                    verify_password, \
                    get_current_user
from settings import settings
from utils.crud import users


router = APIRouter(
    prefix="/api",
    tags=["users"],
)

@router.post('/register')
def register(
    username: str = Form(default=None, max_length=50), 
    password: str = Form(default=None, max_length=50), 
    db: Session = Depends(get_db)
    ):
    
    user = UserFront(username=username, password=password)
    if users.create_user(user, db) is None:
        raise HTTPException(
            status_code=400, 
            detail="User already exists"
            )

    return {"message": "User created successfully"}


@router.post("/login")
async def login(
    response: Response,
    username: str = Form(default=None, max_length=50), 
    password: str = Form(default=None, max_length=50), 
    db: Session = Depends(get_db)
    ):
        
    user = users.get_user_by_username(username, db)
    if not user:
        raise credentials_exception

    correct_password = verify_password(password, user)
    if not correct_password:
        raise credentials_exception

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token: str = create_access_token(
        data={"sub": user.username}, 
        expires_delta=access_token_expires
        )

    response.set_cookie(
        key="Authorization", 
        value=access_token, 
        httponly=True, 
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60, 
        secure=True,
        )
    response.set_cookie(
        key="username",
        value=user.username,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        secure=True,
        )

    return {'message': 'Authenticated'}

@router.get("/logout")
async def logout(response: Response):
    response.set_cookie(
        key="Authorization", 
        value="", 
        httponly=True, 
        max_age=0, 
        secure=True,
        ) 

    response.set_cookie(
        key="username",
        value="",
        max_age=0,
        secure=True,
        )
    return {'message': 'Logged out'}

@router.get("/user", response_model=SettingsScheme)
async def get_settings(
    request: Request,
    db: Session = Depends(get_db)
    ):

    user = get_current_user(request, db)
    settings = users.get_settings(user.username, db)
    return settings
    
@router.post("/settings")
def update_settings(
    settings_form: SettingsScheme,
    request: Request,
    db: Session = Depends(get_db)
    ):

    user = get_current_user(request, db)

    if not settings_form.user == user.username:
        raise HTTPException(
            status_code=400, 
            detail='Wrong username'
            )

    users.update_settings(settings_form, db)

    return {'message': 'Settings updated successfully'}