from typing import Iterable, cast
from sqlalchemy.orm import Session

from db.models import User as UserModel, Settings as SettingsModel
from db.schemas import UserFront, UserWithTwitter, \
    UserInDB, Settings as SettingsScheme
from security import hash_password
from utils.crud.base import unique

def get_twitter_users(
    db: Session
    ) -> Iterable[UserWithTwitter]:

    q: Iterable[tuple[UserInDB, SettingsScheme]] = db.query(
        UserModel, SettingsModel).filter(
        SettingsModel.twitter_header is not None,
        ).join(UserModel).all()

    users: Iterable[UserWithTwitter] = []

    for user, settings in q:
        if settings.twitter_header == '' or settings.twitter_header is None:
            continue
        
        users.append(UserWithTwitter(
            username=user.username,
            twitter_header=settings.twitter_header,
        ))

    return users

def get_user_with_twitter(
    username: str, db: Session
    ) -> UserWithTwitter:

    user_in_db = db.query(UserModel, SettingsModel).filter(
        SettingsModel.user == username,
        ).join(UserModel).first()
    user_in_db = cast(tuple[UserInDB, SettingsScheme], user_in_db)
    user_in_db[1].twitter_header = cast(str, user_in_db[1].twitter_header)

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
    ) -> UserInDB | None:

    user = db.query(UserModel).filter_by(username=username).first()
    return user

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

def update_settings(
    settings_form: SettingsScheme, 
    db: Session
    ) -> SettingsScheme:

    db_settings: SettingsScheme = db.query(
        SettingsModel).filter_by(user=settings_form.user).update(
        {
            'twitter_header': settings_form.twitter_header,
            'authors_blacklist': settings_form.authors_blacklist,
            'tags_blacklist': settings_form.tags_blacklist
        })
    db.commit()
    return db_settings