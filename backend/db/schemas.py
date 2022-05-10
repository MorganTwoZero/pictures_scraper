from datetime import datetime
from pydantic import BaseModel


class PostCreate(BaseModel):
    post_link: str    
    preview_link: str
    images_number: int = 1    
    author: str
    author_link: str
    author_profile_image: str = ''
    source: str
    created: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    token: str
    user: str
    expires: datetime
    token_type: str = 'bearer'


class User(BaseModel):
    user_name: str
    settings: str | None = None # set defalts from env variables

    class Config:
        orm_mode = True


class UserIn(User):
    password: str


class UserOut(User):
    token: Token