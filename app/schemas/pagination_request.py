from pydantic import BaseModel

class PaginatedSchema(BaseModel):
    page: int = 1
    size: int = 10