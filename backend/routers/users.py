from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.db.schemas import UserFront, Settings as SettingsScheme
from backend.dependency import get_db
from backend.exceptions import credentials_exception
from backend.security import create_access_token, \
                    verify_password, \
                    get_current_user
from backend.settings import settings
from backend.utils.crud import users


router = APIRouter(
    prefix="/api",
    tags=["users"],
)

@router.post('/register')
def register(user: UserFront, db: Session = Depends(get_db)):

    if users.create_user(user, db) is None:
        raise HTTPException(status_code=400, detail="User already exists")

    return {"message": "User created successfully"}


@router.post("/login")
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
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    users.update_settings(settings_form, db)

    return {'message': 'Settings updated successfully'}