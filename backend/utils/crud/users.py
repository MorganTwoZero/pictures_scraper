from sqlalchemy.orm import Session

from db.models import User as UserModel
from db.schemas import UserIn, UserDB
from security import hash_password


def _unique(user_name: str, db: Session) -> bool:
    return db.query(UserModel).filter_by(username=user_name).first() == None

def get_user_by_username(username: str, db: Session) -> UserDB:
    return db.query(UserModel).filter_by(username=username).first()

def create_user(user: UserIn, db: Session) -> UserDB | None:
    if _unique(user.username, db):
        db_user: UserDB = UserModel(username=user.username, 
            hashed_password=hash_password(user.password))
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user