import asyncio
import logging
import logging.config

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.testclient import TestClient
import uvicorn
from rocketry import Rocketry
from rocketry.conds import cron

from db.database import engine
from db.base_class import Base
from routers.embed import router as embed_router
from routers.site import router as site_router
from routers.users import router as users_router
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
        settings.SITE_URL,
        ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app_rocketry = Rocketry(config={"task_execution": "async"})

@app.on_event("startup")
@app_rocketry.task(cron(minute='*/20'))
async def fill_db_on_startup():
    '''
    Ugly hack to update on startup and timeout
    because of the way Depends() works
    '''
    client = TestClient(app)
    client.get("/api/update")

class Server(uvicorn.Server):
    """Customized uvicorn.Server
    
    Uvicorn server overrides signals and we need to include
    Rocketry to the signals."""
    def handle_exit(self, sig: int, frame) -> None:
        app_rocketry.session.shut_down()
        return super().handle_exit(sig, frame)

async def main():
    "Run Rocketry and FastAPI"
    server = Server(config=uvicorn.Config(
        app, 
        loop="asyncio",
        access_log=False,
        host='0.0.0.0',
        port=8000
    ))

    api = asyncio.create_task(server.serve())
    sched = asyncio.create_task(app_rocketry.serve())

    await asyncio.wait([sched, api])

if __name__ == "__main__":
    # Print Rocketry's logs to terminal
    logger = logging.getLogger("rocketry.task")

    # Run both applications
    asyncio.run(main())