from typing import Annotated

from fastapi import APIRouter, Depends

from app.services.auth import AuthService

from app.schemas.user.user_request import UserCreate
from app.schemas.auth.auth_response import TokenResponse
from app.schemas.auth.auth_request import LoginRequest, RefreshRequest
from app.schemas.response import ApiResponse, ok

from app.dependencies.auth import get_auth_service

router = APIRouter(tags=["Auth"])

@router.post("/register", response_model=ApiResponse[TokenResponse], status_code=201)
async def register(
    data: UserCreate,
    service: Annotated[AuthService, Depends(get_auth_service)],
):
    result = await service.register(data)
    
    return ok(result, "User registered successfully")

@router.post("/login", response_model=ApiResponse[TokenResponse])
async def login(
    data: LoginRequest,
    service: Annotated[AuthService, Depends(get_auth_service)],
):
    result = await service.login(data)
    
    return ok(result, "Login successful")

@router.post("/refresh", response_model=ApiResponse[TokenResponse])
async def refresh(
    data: RefreshRequest,
    service: Annotated[AuthService, Depends(get_auth_service)],
):
    result = await service.refresh(data)
    
    return ok(result, "Token refreshed successfully")
