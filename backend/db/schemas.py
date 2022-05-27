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
    user: str
    twitter_header: str | None = None
    authors_blacklist: str
    tags_blacklist: str

    class Config:
        orm_mode = True

class RequestResults(BaseModel):
    pixiv: list[dict] | None
    twitter_honkai: list[dict] | None
    twitter_homeline: list[dict] | None
    bbs_mihoyo: list[dict] | None
    lofter: list[str | None]