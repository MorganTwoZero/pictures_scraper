from sqlalchemy.orm import Session
from sqlalchemy import desc

from db.schemas import PostCreate
from db.models import Post as PostModel
from db.database import SessionLocal

db = SessionLocal()

def get_posts(db: Session, page, offset, route):
    page = page - 1
    if route == 'homeline':
        return db.query(PostModel).order_by(desc(PostModel.created)).filter_by(source='homeline').offset(page * offset).limit(offset).all()
    else:
        return db.query(PostModel).order_by(desc(PostModel.created)).filter(PostModel.source!='homeline').offset(page * offset).limit(offset).all()

def get_homeline(db: Session, page, offset):
    page = page - 1
    return db.query(PostModel).order_by(desc(PostModel.created)).filter_by(source='homeline').offset(page * offset).limit(offset).all()

def save_to_db(post: PostCreate):
    db_post = PostModel(**post.dict())
    if db_post.get_unique(db):
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post