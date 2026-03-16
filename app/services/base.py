from math import ceil
from typing import Generic, TypeVar, List, Optional, Type
from pydantic import BaseModel
from starlette import status
from starlette.exceptions import HTTPException

from app.repositories.base import BaseRepository
from app.schemas.pagination_response import PaginatedResponse

ModelType = TypeVar("ModelType", bound=BaseModel)
ResponseType = TypeVar("ResponseType", bound=BaseModel)

class BaseService(Generic[ModelType, ResponseType]):
    def __init__(self, repository: BaseRepository[ModelType]):
        self.repository = repository
    
    @property
    def response_class(self) -> Type[ResponseType]:
        raise NotImplementedError("Subclass must implement response_class property")

    async def create(self, data: ModelType) -> ResponseType:
        document = await self.repository.create(data)
        
        return self._to_response(document)

    async def get_by_id(self, id: str) -> Optional[ResponseType]:
        document = await self.repository.find_by_id(id)
        
        if not document:
            return None
        
        return self._to_response(document)

    async def get_by_external_id(self, id: str) -> ResponseType:
        document = await self._check_document_by_external_id(id)
        
        return self._to_response(document)

    async def get_all(self) -> List[ResponseType]:
        documents = await self.repository.find_all()
        
        return [self._to_response(doc) for doc in documents]

    async def get_paginated(self, page: int = 1, size: int = 10) -> PaginatedResponse:
        documents, total = await self.repository.find_paginated(page=page, size=size)
        
        items = [self._to_response(doc) for doc in documents]
        
        total_pages = ceil(total / size) if size > 0 else 0
        
        return PaginatedResponse(
            items=items,
            total=total,
            page=page,
            size=size,
            total_pages=total_pages
        )

    async def update(self, id: str, data: dict) -> ResponseType:
        document = await self._check_document_by_external_id(id)
        
        updated_document = await self.repository.update(
            document.id,
            data
        )
        
        return self._to_response(updated_document)
    
    async def delete(self, id: str) -> bool:
        document = await self._check_document_by_external_id(id)
        
        return await self.repository.delete(document.id)
    
    # Helper methods
    def _to_response(self, document: ModelType) -> ResponseType:
        if hasattr(self.response_class, 'to_response'):
            return self.response_class.to_response(document.model_dump())
        
        return document
    
    async def _check_document_by_external_id(self, id: str) -> ModelType:
        document = await self.repository.find_by_external_id(id)
        
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found"
            )
        
        return document