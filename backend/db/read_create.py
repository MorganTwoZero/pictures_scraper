from sqlalchemy.orm import Session
from sqlalchemy import desc

from backend.db.models import Post
from backend.db.database import SessionLocal

db = SessionLocal()

def get_posts(db: Session, page, offset):
    page = page - 1
    return db.query(Post).order_by(desc(Post.created)).filter(Post.source!='homeline').offset(page * offset).limit(offset).all()

def get_homeline(db: Session, page, offset):
    page = page - 1
    return db.query(Post).order_by(desc(Post.created)).filter_by(source='homeline').offset(page * offset).limit(offset).all()

def save_to_db(post):
    db_post = Post(**post.dict())
    if db_post.get_unique(db):
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post