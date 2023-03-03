import datetime

from sqlalchemy.orm import Session

from utils.crud import posts
from db.schemas import PostScheme
from db.models import HonkaiPost, TwitterFeedPost


post = {
        'post_link':'https://twitter.com/Rax__4y/status/1545026052564860928/', 
        'preview_link':'https://pbs.twimg.com/media/FXEJAVJaIAADD8A.jpg', 
        'images_number':1, 
        'author':'Rax__4y', 
        'author_link':'https://twitter.com/Rax__4y', 
        'author_profile_image':None, 
        'created':datetime.datetime(2022, 7, 7, 14, 44, 50)
}

def test_db_posts_save_post(db_session: Session):
    for table in [HonkaiPost, TwitterFeedPost]:
        db_post = posts.save_post(PostScheme(**post), db_session, table)
        assert db_post
        db_post = {
            'post_link':db_post.post_link, 
            'preview_link':db_post.preview_link, 
            'images_number':db_post.images_number, 
            'author':db_post.author, 
            'author_link':db_post.author_link, 
            'author_profile_image':db_post.author_profile_image, 
            'created':db_post.created
        }
        assert db_post == post

def test_db_posts_unique_check(db_session: Session):
    posts.save_post(PostScheme(**post), db_session, HonkaiPost)
    assert posts.save_post(PostScheme(**post), db_session, HonkaiPost) is None