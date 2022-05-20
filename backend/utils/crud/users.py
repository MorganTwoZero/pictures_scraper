from sqlalchemy.orm import Session

from db.models import User as UserModel
from db.schemas import UserFront, UserInDB
from security import hash_password
from utils.crud.base import unique


def get_user_by_username(username: str, db: Session) -> UserInDB:
    return db.query(UserModel).filter_by(username=username).first()

def create_user(user: UserFront, db: Session) -> UserInDB | None:
    if unique(UserModel, db, 'username', user.username):
        db_user: UserInDB = UserModel(username=user.username, 
            hashed_password=hash_password(user.password))
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user