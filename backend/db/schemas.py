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
    source: str

    class Config:
        orm_mode = True