
from fastapi import APIRouter

from app.core.config import settings

router = APIRouter(tags=["Health"])

@router.get("/health", summary="Health check")
async def health():
    return {
        "status": "ok",
        "title": settings.api_title,
        "version": settings.api_version,
        "description": settings.api_description
    }