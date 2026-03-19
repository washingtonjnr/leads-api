from app.models.lead import Lead
from app.repositories.base import BaseRepository

from app.core.types import IODatabase

class LeadRepository(BaseRepository[Lead]):
    def __init__(self, db: IODatabase):
        super().__init__(db, Lead, "leads")

    async def get_by_email(self, email: str):
        doc = await self.collection.find_one(
            {"email": email}
        )

        if not doc:
            return None

        return Lead(**doc)
