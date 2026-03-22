from fastapi import APIRouter

from app.core.config import settings
from app.schemas.response import ApiResponse, ok

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=ApiResponse, summary="Health check")
async def health():
    return ok({
        "status": "ok",
        "title": settings.api_title,
        "version": settings.api_version,
        "description": settings.api_description,
    })
