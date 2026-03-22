from pydantic import BaseModel, Field

class PaginatedSchema(BaseModel):
    page: int = Field(1, ge=1, description="Page")
    size: int = Field(10, ge=1, description="Items per page")