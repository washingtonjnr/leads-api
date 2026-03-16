from fastapi import APIRouter

from .lead import router as leads_router
from .health import router as health_router

routers: list[APIRouter] = [
    leads_router,
    health_router
]