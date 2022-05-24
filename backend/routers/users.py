from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from db.schemas import UserOut, UserFront
from dependency import get_db
from exceptions import credentials_exception
from security import create_access_token, verify_password, verify_token
from settings import settings
from utils.crud import users


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
        samesite='Strict',
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
        samesite='Strict',
        secure=True,
        ) 
    return {'message': 'Logged out'}

@router.get("/user", response_model=UserOut)
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
