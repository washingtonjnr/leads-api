from typing import Annotated

from fastapi import APIRouter, Depends

from app.services.auth import AuthService

from app.schemas.user.user_request import UserCreate
from app.schemas.user.user_response import UserResponse
from app.schemas.auth.auth_response import TokenResponse
from app.schemas.auth.auth_request import LoginRequest, RefreshRequest

from app.dependencies.auth import get_auth_service

router = APIRouter(tags=["Auth"])

@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(
    data: UserCreate,
    service: Annotated[AuthService, Depends(get_auth_service)],
):
    return await service.register(data)


@router.post("/login", response_model=TokenResponse)
async def login(
    data: LoginRequest,
    service: Annotated[AuthService, Depends(get_auth_service)],
):
    return await service.login(data)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    data: RefreshRequest,
    service: Annotated[AuthService, Depends(get_auth_service)],
):
    return await service.refresh(data)
