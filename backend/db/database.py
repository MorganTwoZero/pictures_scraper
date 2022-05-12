from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.base_class import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}, 
)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)
base = Base.metadata.create_all(bind=engine) # type: ignore