from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.testclient import TestClient
from fastapi_utils.tasks import repeat_every

from db.database import Base, engine
from routers.imports import *
from scrapers.imports import *
from settings import settings


Base.metadata.create_all(bind=engine) # type: ignore

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

app = FastAPI()
app.include_router(embed_router)
app.include_router(site_router)
app.include_router(users_router)

client = TestClient(app)

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
def test_update():
    '''
    Ugly hack to update on startup and timeout
    because of the way Depends() works
    '''
    client.get("/api/update")