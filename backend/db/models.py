from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from db.base_class import Base


class Post(Base): # type: ignore
    __tablename__ = "posts"

    post_link = Column(String, index=True, primary_key=True, 
    unique=True)
    preview_link = Column(String, nullable=True, default=None)
    images_number = Column(Integer)
    created = Column(DateTime)
    author = Column(String, nullable=True, default=None)
    author_link = Column(String, nullable=True, default=None)
    author_profile_image = Column(String, nullable=True, 
    default=None)
    source = Column(String)

class User(Base): # type: ignore
    __tablename__ = "users"

    username = Column(String, index=True, 
    primary_key=True, unique=True)
    hashed_password = Column(String)

class Token(Base): # type: ignore
    __tablename__ = "tokens"

    token = Column(String)
    username = Column(ForeignKey("users.username"), index=True, 
    primary_key=True)
