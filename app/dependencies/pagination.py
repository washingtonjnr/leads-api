from fastapi import Query
from app.schemas.pagination_request import PaginatedSchema

def get_pagination(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Items per page"),
) -> PaginatedSchema:
    return PaginatedSchema(page=page, size=size)