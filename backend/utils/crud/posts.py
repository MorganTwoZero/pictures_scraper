from sqlalchemy.orm import Session
from sqlalchemy import desc

from db.schemas import PostCreate
from db.models import Post as PostModel
from utils.crud.base import unique


def get_posts(db: Session, page, offset, route):
    page = page - 1
    routes = {
        'honkai': True,
        'homeline': False
    }
    return db.query(PostModel).order_by(desc(PostModel.created)
        ).filter_by(honkai=routes[route]
        ).offset(page * offset).limit(offset).all()

def save_to_db(post: PostCreate, db: Session):
    db_post = PostModel(**post.dict())
    if unique(PostModel, db, 'post_link', post.post_link):
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post