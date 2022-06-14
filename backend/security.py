from datetime import datetime, timedelta

from fastapi import Request, HTTPException
from passlib.context import CryptContext
from jose import JWTError, jwt

from backend.db.schemas import UserInDB
import backend.utils.crud.users as users
from backend.settings import settings
from backend.exceptions import credentials_exception


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username

def create_access_token(data: dict, 
        expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt: str = jwt.encode(to_encode, settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM)
    return encoded_jwt

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, user: UserInDB) -> bool:
    return pwd_context.verify(plain_password, user.hashed_password)

def get_current_user(request: Request, db) -> UserInDB:
    token = request.cookies.get('Authorization')
    if not token:
        raise HTTPException(status_code=204, detail="User not found")

    username = verify_token(token)
    if not username:
        raise HTTPException(status_code=400, detail="Invalid token")

    user = users.get_user_by_username(username, db)
    if not user:
        raise HTTPException(status_code=204, detail="User not found")
        
    return user