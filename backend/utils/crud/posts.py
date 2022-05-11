from sqlalchemy.orm import Session
from sqlalchemy import desc

from db.schemas import PostCreate
from db.models import Post as PostModel


def _unique(post_link: str, db: Session) -> bool:
    return db.query(PostModel).filter_by(post_link=post_link).first() == None

def get_posts(db: Session, page, offset, route):
    page = page - 1
    if route == 'homeline':
        return db.query(PostModel).order_by(desc(PostModel.created)
            ).filter_by(source='homeline'
            ).offset(page * offset).limit(offset).all()
    else:
        return db.query(PostModel).order_by(desc(PostModel.created)
            ).filter(PostModel.source!='homeline'
            ).offset(page * offset).limit(offset).all()

def get_homeline(db: Session, page, offset):
    page = page - 1
    return db.query(PostModel).order_by(desc(PostModel.created)
        ).filter_by(source='homeline'
        ).offset(page * offset).limit(offset).all()

def save_to_db(post: PostCreate, db: Session):
    db_post = PostModel(**post.dict())
    if _unique(post.post_link, db):
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post