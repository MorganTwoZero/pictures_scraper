from typing import Generator

from sqlalchemy.orm import Session

from backend.db.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    try:
        db: Session = SessionLocal()
        yield db
    finally:
        db.close()  # type: ignore