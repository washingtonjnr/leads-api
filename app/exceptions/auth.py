from fastapi import status
from app.exceptions.base import AppException

class NotAuthenticatedException(AppException):
    def __init__(self):
        super().__init__("Not authenticated", status.HTTP_401_UNAUTHORIZED)

class InvalidCredentialsException(AppException):
    def __init__(self):
        super().__init__("Invalid credentials", status.HTTP_401_UNAUTHORIZED)

class TokenExpiredException(AppException):
    def __init__(self):
        super().__init__("Token expired", status.HTTP_401_UNAUTHORIZED)

class InvalidTokenException(AppException):
    def __init__(self):
        super().__init__("Invalid token", status.HTTP_401_UNAUTHORIZED)
