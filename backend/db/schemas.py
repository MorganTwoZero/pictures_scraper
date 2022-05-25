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
    twitter_header: str
    blacklist_authors: str
    blacklist_tags: str

    class Config:
        orm_mode = True