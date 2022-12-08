from datetime import datetime

from pydantic import BaseModel, validator


class PostScheme(BaseModel):
    post_link: str    
    preview_link: str
    images_number: int = 1    
    author: str
    author_link: str
    author_profile_image: str | None = None
    created: datetime

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

class UserWithTwitter(User):
    twitter_header: str

class UserInDB(User):
    hashed_password: str

class SettingsBase(BaseModel):
    twitter_header: str | None = None
    authors_blacklist: str
    tags_blacklist: str

    @validator('twitter_header')
    def proper_header(cls, v):
        if v is not None:
            headers = [
                'authorization',
                'cookie',
                'auth_token',
                'ct0',
                'Bearer',
                'x-csrf-token',
            ]
            if not all(h in v for h in headers):
                raise ValueError('Missing some value in header')
        return v

class Settings(SettingsBase):
    user: str

    class Config:
        orm_mode = True

class SettingsPatch(SettingsBase):
    pass

class RequestResults(BaseModel):
    pixiv: list[dict] | None
    twitter_honkai: list[dict] | None
    bbs_mihoyo: list[dict] | None
    lofter: list[str | None]
    bcy: list[dict]