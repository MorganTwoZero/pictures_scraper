from datetime import datetime

from pydantic import BaseModel


class PostCreate(BaseModel):
    post_link: str    
    preview_link: str
    images_number: int = 1    
    author: str
    author_link: str
    author_profile_image: str | None = None
    created: datetime
    honkai: bool

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
    
    class Config:
        orm_mode = True

class UserIn(User):
    password: str

class UserDB(User):
    hashed_password: str
