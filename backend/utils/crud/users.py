from typing import Iterable, cast, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import Row

from db.models import User as UserModel, Settings as SettingsModel
from db.schemas import UserFront, UserWithTwitter, \
    UserInDB, Settings as SettingsScheme
from security import hash_password
from utils.crud.base import unique

def get_twitter_users(
    db: Session
    ) -> Iterable[UserWithTwitter]:

    q: List[Row[Tuple[UserModel, SettingsModel]]] = db.query(
        UserModel, SettingsModel).filter(
        SettingsModel.twitter_header.isnot(None),
        ).join(UserModel).all()

    users: Iterable[UserWithTwitter] = []

    for user, settings in q:
        users.append(UserWithTwitter(
            username=user.username,
            twitter_header=settings.twitter_header,
        ))

    return users

def get_user_with_twitter(
    username: str, db: Session
    ) -> UserWithTwitter | None:

    user_in_db = db.query(UserModel, SettingsModel).filter(
        SettingsModel.user == username,
        SettingsModel.twitter_header.isnot(None),
        ).join(UserModel).first()

    if user_in_db is not None:
        user_with_twitter = UserWithTwitter(
            username=user_in_db[0].username,
            twitter_header=user_in_db[1].twitter_header,
        )        
        return user_with_twitter

def get_settings(username: str, db: Session) -> SettingsScheme:
    settings = db.query(SettingsModel).filter_by(user=username).first()
    settings = cast(SettingsScheme, settings)
    return settings

def get_user_by_username(
    username: str, 
    db: Session
    ) -> UserModel | None:

    user = db.query(UserModel).filter_by(username=username).first()
    return user

def create_user(user: UserFront, db: Session) -> UserModel | None:
    if unique(UserModel, db, 'username', user.username):
        db_user = UserModel(username=user.username, 
            hashed_password=hash_password(user.password))
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        settings = SettingsModel(
            user=user.username
            )
        db.add(settings)
        db.commit()
        db.refresh(settings)
        return db_user
    return None

def update_settings(
    settings_form: SettingsScheme, 
    db: Session
    ) -> SettingsScheme:

    db_settings = db.query(
        SettingsModel).filter_by(user=settings_form.user).update(
        {
            'twitter_header': settings_form.twitter_header,
            'authors_blacklist': settings_form.authors_blacklist,
            'tags_blacklist': settings_form.tags_blacklist
        })
    db.commit()
    return db_settings