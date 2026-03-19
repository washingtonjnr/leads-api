from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status

from app.models.user import User
from app.models.refresh_token import RefreshTokenModel

from app.repositories.user import UserRepository
from app.repositories.refresh_token import RefreshTokenRepository

from app.schemas.auth.auth_request import LoginRequest, RefreshRequest
from app.schemas.auth.auth_response import TokenResponse
from app.schemas.user.user_request import UserCreate

from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from app.core.config import settings

class AuthService:
    def __init__(self, user_repo: UserRepository, token_repo: RefreshTokenRepository):
        self.user_repo = user_repo
        self.token_repo = token_repo

    async def _generate_tokens(self, user_id: str) -> TokenResponse:
        access_token = create_access_token(user_id)
        refresh_token = create_refresh_token(user_id)

        token_record = RefreshTokenModel(
            token=refresh_token,
            user_id=user_id,
            expires_at=datetime.now(timezone.utc) + timedelta(days=settings.jwt_refresh_expire_days),
        )

        await self.token_repo.create(token_record)

        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    async def register(self, data: UserCreate) -> TokenResponse:
        existing = await self.user_repo.get_by_email(data.email)

        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

        user = User(
            name=data.name,
            email=data.email,
            hashed_password=hash_password(data.password),
        )

        created = await self.user_repo.create(user)

        return await self._generate_tokens(created.external_id)

    async def login(self, data: LoginRequest) -> TokenResponse:
        user = await self.user_repo.get_by_email(data.email)

        if not user or not verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        return await self._generate_tokens(user.external_id)

    async def refresh(self, data: RefreshRequest) -> TokenResponse:
        stored = await self.token_repo.get_by_token(data.refresh_token)

        if not stored or stored.revoked:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

        if stored.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired")

        try:
            payload = decode_token(data.refresh_token, expected_type="refresh")
        except Exception:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

        await self.token_repo.revoke(data.refresh_token)

        subject = payload.get("sub")
        
        new_access = create_access_token(subject)
        new_refresh = create_refresh_token(subject)

        token_record = RefreshTokenModel(
            token=new_refresh,
            user_id=subject,
            expires_at=datetime.now(timezone.utc) + timedelta(days=settings.jwt_refresh_expire_days),
        )
        
        await self.token_repo.create(token_record)

        return TokenResponse(access_token=new_access, refresh_token=new_refresh)
