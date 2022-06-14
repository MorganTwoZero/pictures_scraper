from typing import Iterable
from sqlalchemy.orm import Session

from db.models import User as UserModel, Settings as SettingsModel
from db.schemas import UserFront, UserWithTwitter ,UserInDB, Settings as SettingsScheme
from security import hash_password
from utils.crud.base import unique

def get_all_users_with_twitter(db: Session) -> Iterable[UserWithTwitter]:

    q: Iterable[tuple[UserInDB, SettingsScheme]] = db.query(UserModel, SettingsModel).filter(
        SettingsModel.twitter_header != None,
        ).join(UserModel).all()  # type: ignore

    users: Iterable[UserWithTwitter] = []

    for user, settings in q:
        assert settings.twitter_header
        
        users.append(UserWithTwitter(
            username=user.username,
            twitter_header=settings.twitter_header,
        ))

    return users

def get_user_with_twitter(username: str, db: Session) -> UserWithTwitter:

    user_in_db = db.query(UserModel, SettingsModel).filter(
        SettingsModel.user == username,
        ).join(UserModel).first()  # type: ignore

    user_with_twitter: UserWithTwitter = UserWithTwitter(
        username=user_in_db.User.username,  # type: ignore
        twitter_header=user_in_db.Settings.twitter_header,  # type: ignore
    )

    return user_with_twitter

def get_settings(username: str, db: Session) -> SettingsScheme:
    query = db.query(SettingsModel).filter_by(user=username)
    return query.first()

def get_user_by_username(username: str, db: Session) -> UserInDB:
    return db.query(UserModel).filter_by(username=username).first()

def create_user(user: UserFront, db: Session) -> UserInDB | None:
    if unique(UserModel, db, 'username', user.username):
        db_user: UserInDB = UserModel(username=user.username, 
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

def update_settings(settings_form: SettingsScheme, db: Session) -> SettingsScheme:
    db_settings: SettingsScheme = db.query(SettingsModel).filter_by(user=settings_form.user).update(
        {
            'twitter_header': settings_form.twitter_header,
            'authors_blacklist': settings_form.authors_blacklist,
            'tags_blacklist': settings_form.tags_blacklist
        })
    db.commit()
    return db_settings