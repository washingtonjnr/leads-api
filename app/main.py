from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import connect_to_mongo, close_mongo_connection
from app.migrations.runner import run_migrations

from app.controllers import routers

@asynccontextmanager
async def lifespan(_: FastAPI):
    connect_to_mongo()
    
    await run_migrations()
    
    yield
    
    close_mongo_connection()

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.api_title,
        version=settings.api_version,
        description=settings.api_description,
        lifespan=lifespan 
    )

    for router in routers:
        app.include_router(router)

    return app

app = create_app()