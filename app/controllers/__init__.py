from fastapi import APIRouter

from .auth import router as auth_router
from .lead import router as leads_router
from .health import router as health_router
from .jira import router as jira_router

routers: list[APIRouter] = [
    auth_router,
    leads_router,
    health_router,
    jira_router,
]