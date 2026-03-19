from typing import Optional

from app.models.refresh_token import RefreshTokenModel
from app.repositories.base import BaseRepository
from app.core.types import IODatabase

class RefreshTokenRepository(BaseRepository[RefreshTokenModel]):
    def __init__(self, db: IODatabase):
        super().__init__(db, RefreshTokenModel, "refresh_tokens")

    async def get_by_token(self, token: str) -> Optional[RefreshTokenModel]:
        token = await self.collection.find_one({ "token": token })

        if not token:
            return None

        return RefreshTokenModel(**token)

    async def revoke(self, token: str) -> bool:
        result = await self.collection.update_one(
            {"token": token},
            {"$set": {"revoked": True}}
        )
        return result.modified_count > 0
