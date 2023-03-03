import ast
from typing import Generator

from httpx import AsyncClient
from sqlalchemy.orm import Session

from db.database import SessionLocal
from settings import settings


def get_db() -> Generator[Session, None, None]:
    try:
        db: Session = SessionLocal()
        yield db
    finally:
        db.close()  # type: ignore

def get_request_client() -> AsyncClient:
    client = AsyncClient(headers=ast.literal_eval(settings.HEADER), timeout=10, follow_redirects=True)
    return client