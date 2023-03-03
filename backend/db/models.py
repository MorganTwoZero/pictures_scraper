from sqlalchemy import Column, DateTime, Integer, String

from db.base_class import Base


class BasePost:
    post_link = Column(String, index=True, primary_key=True, 
        unique=True)
    preview_link = Column(String, nullable=True, default=None)
    images_number = Column(Integer)
    created = Column(DateTime, index=True)
    author = Column(String, nullable=True, default=None)
    author_link = Column(String, nullable=True, default=None)
    author_profile_image = Column(String, nullable=True, 
        default=None)

class HonkaiPost(Base, BasePost): # type: ignore
    __tablename__ = "posts" # type: ignore
    __table_args__ = {'extend_existing': True}

class TwitterFeedPost(Base, BasePost): # type: ignore
    __tablename__ = "twitter_feed_posts" # type: ignore
    __table_args__ = {'extend_existing': True}