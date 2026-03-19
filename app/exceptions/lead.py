from fastapi import status
from app.exceptions.base import AppException

class LeadNotFoundException(AppException):
    def __init__(self):
        super().__init__("Lead not found", status.HTTP_404_NOT_FOUND)

class LeadAlreadyExistsException(AppException):
    def __init__(self):
        super().__init__("Email already registered", status.HTTP_409_CONFLICT)
