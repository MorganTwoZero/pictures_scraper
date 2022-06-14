from typing import Iterable
from sqlalchemy.orm import Session

from backend.db.schemas import PostScheme, TwitterPostScheme, User as UserScheme
from backend.db.models import Post as PostModel, TwitterFeedPost, User as UserModel
from backend.utils.crud.base import unique


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

def save_post_many_users(db: Session, post: TwitterPostScheme, user: UserScheme):

    db_post = TwitterFeedPost(**post.dict())
    
    #Already asserted that user is in db, so no need to check
    user_in_db: UserModel = db.query(UserModel).filter(UserModel.username == user.username)[0]

    post_in_db = db.query(TwitterFeedPost).filter(TwitterFeedPost.post_link == db_post.post_link).first()

    if post_in_db is None:
        db.add(db_post)        
        db.commit()
        db.refresh(db_post)
        return db_post

    if not user_in_db in post_in_db.users:
        post_in_db.users.append(user_in_db)
        db.commit()
        db.refresh(post_in_db)
        return post_in_db