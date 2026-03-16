import uuid

from pydantic import BaseModel
from typing import Generic, TypeVar, Type, List, Optional

from app.core.types import IODatabase
from app.utils.sequence import get_next_sequence

ModelType = TypeVar("ModelType", bound=BaseModel)

class BaseRepository(Generic[ModelType]):
    def __init__(
        self,
        db: IODatabase,
        model: Type[ModelType],
        collection_name: str,
    ):
        self.db = db
        self.model = model
        self.collection = db[collection_name]
        self.collection_name = collection_name

    async def create(self, data: BaseModel) -> ModelType:
        payload = data.model_dump(by_alias=True, exclude={"id"})
        
        next_id = await get_next_sequence(self.db, self.collection_name)
        payload["_id"] = next_id
        
        payload["external_id"] = str(uuid.uuid4())
        
        await self.collection.insert_one(payload)
        
        payload["id"] = next_id
        return self.model(**payload)

    async def find_by_id(self, id: str) -> Optional[ModelType]:
        document = await self.collection.find_one(
            {"_id": int(id)}
        )

        if not document:
            return None

        return self.model(**document)

    async def find_by_external_id(self, id: str) -> Optional[ModelType]:
        document = await self.collection.find_one(
            {"external_id": id}
        )

        if not document:
            return None

        return self.model(**document)

    async def find_all(self) -> List[ModelType]:
        documents = []

        async for doc in self.collection.find():
            documents.append(self.model(**doc))

        return documents

    async def find_paginated(self, page: int = 1, size: int = 10) -> tuple[List[ModelType], int]:
        skip = (page - 1) * size
        
        total = await self.collection.count_documents({})
        
        documents = []
        async for doc in self.collection.find().skip(skip).limit(size):
            documents.append(self.model(**doc))
        
        return documents, total

    async def update(self, id: str, data: dict) -> Optional[ModelType]:
        await self.collection.update_one(
            {"_id": int(id)},
            {"$set": data},
        )

        return await self.find_by_id(id)

    async def delete(self, id: str) -> bool:
        result = await self.collection.delete_one(
            {"_id": int(id)}
        )

        return result.deleted_count > 0