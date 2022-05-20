from datetime import datetime

from pydantic import BaseModel


class PostScheme(BaseModel):
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

class UserOut(User):
    pass

class UserFront(User):
    password: str

class UserInDB(User):
    hashed_password: str

class Settings(BaseModel):
    username: str
    authors: str
    tags: str
    pixiv_header: str
    twitter_header: str