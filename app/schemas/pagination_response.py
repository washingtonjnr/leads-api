from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from typing import Generic, TypeVar, List

DataType = TypeVar("DataType", bound=BaseModel)

class PaginatedResponse(GenericModel, Generic[DataType]):
    items: List[DataType] = Field(..., description="List of items")
    total: int = Field(..., description="Total number of items")
    page: int = Field(1, ge=1, description="Current page number")
    size: int = Field(10, ge=1, description="Items per page")
    total_pages: int = Field(..., description="Total number of pages")

    model_config = {
        "json_schema_extra": {
            "example": {
                "items": [],
                "total": 100,
                "page": 1,
                "size": 10,
                "total_pages": 10
            }
        }
    }