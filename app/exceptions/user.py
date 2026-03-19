from fastapi import status
from app.exceptions.base import AppException

class UserNotFoundException(AppException):
    def __init__(self):
        super().__init__("User not found", status.HTTP_404_NOT_FOUND)

class UserAlreadyExistsException(AppException):
    def __init__(self):
        super().__init__("Email already registered", status.HTTP_409_CONFLICT)
