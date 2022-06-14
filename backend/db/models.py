from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean, Table
from sqlalchemy.orm import relationship

from backend.db.base_class import Base
from backend.settings import settings


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

association_table = Table(
    "association",
    Base.metadata,  # type: ignore
    Column("posts", ForeignKey("twitter_feed_posts.post_link"), primary_key=True),
    Column("users", ForeignKey("users.username"), primary_key=True),
)

class TwitterFeedPost(Base): # type: ignore
    __tablename__ = "twitter_feed_posts"

    post_link = Column(String, index=True, primary_key=True, 
        unique=True
        )
    preview_link = Column(String, nullable=True, default=None)
    images_number = Column(Integer)
    created = Column(DateTime, index=True)
    author = Column(String, nullable=True, default=None)
    author_link = Column(String, nullable=True, default=None)
    author_profile_image = Column(String, nullable=True, 
        default=None
        )
    users = relationship(
        "User", secondary=association_table, back_populates="posts"
    )

class User(Base): # type: ignore
    __tablename__ = "users"

    username = Column(String, index=True,
        primary_key=True, unique=True)
    hashed_password = Column(String)
    posts = relationship(
        "TwitterFeedPost", secondary=association_table, back_populates="users"
    )

class Settings(Base): # type: ignore
    __tablename__ = "settings"

    user = Column(String, ForeignKey("users.username"), primary_key=True)
    authors_blacklist = Column(String, nullable=True, default=settings.SCARY_AUTHORS)
    tags_blacklist = Column(String, nullable=True, default=settings.SCARY_TAGS)
    twitter_header = Column(String, nullable=True)