from typing import Optional

from app.models.user import User
from app.repositories.base import BaseRepository
from app.core.types import IODatabase

class UserRepository(BaseRepository[User]):
    def __init__(self, db: IODatabase):
        super().__init__(db, User, "users")

    async def get_by_email(self, email: str) -> Optional[User]:
        user = await self.collection.find_one({ "email": email })

        if not user:
            return None

        return User(**user)
