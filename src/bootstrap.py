from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from src.sqla.db.db_service import db_service
from src.core.config import settings
from src.middlewares import apply_middlewares
from src.routers import apply_routers
from src.kafka.kafka_service import kafka_service


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await kafka_service.start()
    yield
    await db_service.dispose()
    await kafka_service.stop()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.fastapi.title,
        description=settings.fastapi.description,
        version=settings.fastapi.version,
        docs_url=settings.fastapi.docs_url,
        redoc_url=settings.fastapi.redoc_url,
        lifespan=lifespan,
    )

    app = apply_routers(apply_middlewares(app))

    return app
