from sqlalchemy import Column, String, DateTime, Integer

from backend.db.database import Base


class Post(Base):
    __tablename__ = "posts"

    post_link = Column(String, index=True, primary_key=True, unique=True)
    preview_link = Column(String, nullable=True, default=None)
    images_number = Column(Integer)
    created = Column(DateTime)
    author = Column(String, nullable=True, default=None)
    author_link = Column(String, nullable=True, default=None)
    author_profile_image = Column(String, nullable=True, default=None)
    source = Column(String)

    def get_unique(self, db):
        return db.query(self.__class__).filter_by(post_link=self.post_link).first() == None