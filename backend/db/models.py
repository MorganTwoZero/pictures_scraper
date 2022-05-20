from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

from db.base_class import Base


class Post(Base): # type: ignore
    __tablename__ = "posts"

    post_link = Column(String, index=True, primary_key=True, 
        unique=True)
    preview_link = Column(String, nullable=True, default=None)
    images_number = Column(Integer)
    created = Column(DateTime, index=True)
    author = Column(String, nullable=True, default=None)
    author_link = Column(String, nullable=True, default=None)
    author_profile_image = Column(String, nullable=True, 
        default=None)
    honkai = Column(Boolean)

class TwitterPost(Base): # type: ignore
    __tablename__ = "twitter_posts"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    preview_link = Column(String, nullable=True, default=None)
    images_number = Column(Integer)
    created = Column(DateTime, index=True)
    author = Column(String, nullable=True, default=None)
    author_link = Column(String, nullable=True, default=None)
    author_profile_image = Column(String, nullable=True, 
        default=None)


class User(Base): # type: ignore
    __tablename__ = "users"

    username = Column(String, index=True, 
        primary_key=True, unique=True)
    hashed_password = Column(String)
    settings = relationship("Settings", back_populates="user", uselist=False)

class Settings(Base): # type: ignore
    __tablename__ = "settings"

    user = relationship("User", back_populates="settings", uselist=False)
    username = Column(String, ForeignKey("users.username"), 
        index=True, primary_key=True)
    authors_blacklist = Column(String, nullable=True, default=None)
    tags_blacklist = Column(String, nullable=True, default=None)
    twitter_header = Column(String, nullable=True, default=None)