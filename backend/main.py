import logging.config

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.testclient import TestClient
from fastapi_utils.tasks import repeat_every

from db.database import engine
from db.base_class import Base
from parsers.imports import *
from routers.imports import *
from settings import settings
from log_settings import LOGGING_CONFIG


logging.config.dictConfig(LOGGING_CONFIG)

Base.metadata.create_all(bind=engine) # type: ignore

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

app = FastAPI()
app.include_router(site_router)
app.include_router(users_router)
app.include_router(embed_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL,
        ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.on_event("startup")
@repeat_every(seconds=60 * settings.UPDATE_TIMEOUT)
def fill_db_on_startup():
    '''
    Ugly hack to update on startup and timeout
    because of the way Depends() works
    '''
    client = TestClient(app)
    client.get("/api/update")