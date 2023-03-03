from sqlalchemy.orm import Session

from db.schemas import PostScheme
from utils.crud.base import unique


def get_posts(
    db: Session, 
    page: int, 
    offset: int,
    table
    ) -> list[PostScheme]:
    page -= 1
    posts: list[PostScheme] = db.query(table
        ).order_by(table.created.desc()
        ).offset(page * offset).limit(offset).all() # type: ignore
    return posts

def save_post(
    post: PostScheme, 
    db: Session, 
    table
    ):
    db_post = table(**post.dict())
    if unique(table, db, 'post_link', post.post_link):
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post