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

    class Config:
        orm_mode = True

class RequestResults(BaseModel):
    pixiv: list[dict] | None
    twitter_honkai: list[dict] | None
    bbs_mihoyo: list[dict] | None
    lofter: list[str | None]
    bcy: list[dict]
    myfeed: list[dict]