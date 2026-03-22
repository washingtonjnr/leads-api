from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    data: Optional[T] = None
    success: bool
    message: str


def ok(data: T, message: str = "success") -> ApiResponse[T]:
    return ApiResponse(data=data, success=True, message=message)
