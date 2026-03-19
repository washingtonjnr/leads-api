from typing import Callable, Awaitable, Optional

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from app.core.security import decode_token

EXEMPT_PATHS: set[str] = {
    "/health",
    "/docs",
    "/openapi.json",
    "/login",
    "/refresh",
    "/register",
}

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        if self._is_exempt_path(request.url.path):
            return await call_next(request)

        token = self._extract_token(request)

        if not token:
            return self._unauthorized("Not authenticated")

        try:
            payload = decode_token(token)
            
            request.state.user_id = payload.get("sub")
        except ExpiredSignatureError:
            return self._unauthorized("Token expired")
        except InvalidTokenError:
            return self._unauthorized("Invalid token")

        return await call_next(request)

    def _is_exempt_path(self, path: str) -> bool:
        return path in EXEMPT_PATHS

    def _extract_token(self, request: Request) -> Optional[str]:
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None

        scheme, _, token = auth_header.partition(" ")

        if scheme.lower() != "bearer" or not token:
            return None

        return token

    def _unauthorized(self, message: str) -> JSONResponse:
        return JSONResponse(
            content={ "data": None, "success": False, "message": message },
            status_code=401,
        )