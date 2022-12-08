from datetime import timedelta

from fastapi import APIRouter, Depends, Form, \
    HTTPException, Response, Request
from sqlalchemy.orm import Session

from db.schemas import UserFront, Settings as SettingsScheme, SettingsPatch
import deps
from exceptions import CredentialsException
import security
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
    db: Session = Depends(deps.get_db)
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
    db: Session = Depends(deps.get_db)
    ):
        
    user = users.get_user_by_username(username, db)
    if not user:
        raise CredentialsException

    correct_password = security.verify_password(password, user)
    if not correct_password:
        raise CredentialsException

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token: str = security.create_access_token(
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
    db: Session = Depends(deps.get_db)
    ):

    user = security.get_current_user(request, db)
    settings = users.get_settings(user.username, db)
    return settings
    
@router.post("/settings")
def update_settings(
    settings_form: SettingsPatch,
    request: Request,
    db: Session = Depends(deps.get_db)
    ):

    user = security.get_current_user(request, db)
    settings = SettingsScheme(
        **settings_form.dict(),
        user=user.username,
    )

    users.update_settings(settings, db)

    return {'message': 'Settings updated successfully'}