import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import settings
from app.controllers import health_controller
from app.database.connection import init_database

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_database()
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

app.include_router(health_controller.router)
