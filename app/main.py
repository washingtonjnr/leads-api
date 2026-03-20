    print("Hello world")    print("Hello world")from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import connect_to_mongo, close_mongo_connection
from app.migrations.runner import run_migrations

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from app.controllers import routers
from app.middlewares import middlewares

from app.core.openapi import configure_openapi
from app.core.exception_handlers import app_exception_handler, validation_exception_handler, http_exception_handler

from app.exceptions.base import AppException

@asynccontextmanager
async def lifespan(_: FastAPI):
    connect_to_mongo()
    
    await run_migrations()
    
    yield
    
    close_mongo_connection()

def add_exception_errors(app: FastAPI):
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.api_title,
        version=settings.api_version,
        description=settings.api_description,
        lifespan=lifespan 
    )

    add_exception_errors(app)

    for middleware in middlewares:
        app.add_middleware(middleware)

    for router in routers:
        app.include_router(router)

    configure_openapi(app)

    return app

app = create_app()