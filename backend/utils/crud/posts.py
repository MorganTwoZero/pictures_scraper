from typing import Iterable
from sqlalchemy.orm import Session

from db.schemas import PostScheme, TwitterPostScheme, User as UserScheme
from db.models import Post as PostModel, TwitterFeedPost, User
from utils.crud.base import unique


def get_posts(db: Session, page: int, offset: int) -> Iterable[PostScheme]:
    page -= 1
    posts: list[PostScheme] = db.query(PostModel).order_by(PostModel.created.desc()).\
        offset(page * offset).limit(offset).all()

    return posts

def my_feed_db_get(db: Session, user: UserScheme, page: int, offset: int) -> Iterable[TwitterPostScheme]:
    page -= 1
    posts: list[TwitterPostScheme] = db.query(TwitterFeedPost).\
        filter(TwitterFeedPost.users.any(username=user.username)).\
        order_by(TwitterFeedPost.created.desc()).\
        offset(page * offset).limit(offset).all()  # type: ignore
    
    return posts

def save_to_db(post: PostScheme, db: Session):
    db_post = PostModel(**post.dict())
    if unique(PostModel, db, 'post_link', post.post_link):
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post

def save_to_db_many_users(db: Session, post: TwitterPostScheme, user: UserScheme):

    db_post = TwitterFeedPost(**post.dict())
    
    user_instance = db.query(User).filter(User.username == user.username).first()
    assert user_instance
    user = user_instance

    post_in_db = db.query(TwitterFeedPost).filter(TwitterFeedPost.post_link == db_post.post_link).first()

    if post_in_db is None:
        db.add(db_post)        
        db.commit()
        db.refresh(db_post)
        return db_post

    if not user in post_in_db.users:
        post_in_db.users.append(user)
        db.commit()
        db.refresh(post_in_db)
        return post_in_db