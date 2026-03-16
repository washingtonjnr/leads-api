from app.core.config import settings
from app.providers.base import BaseProvider
from app.schemas.dummyjson.user_response import DummyUserResponse, DummyUserSearchResponse

class DummyJSONProvider(BaseProvider):
    def __init__(self):
        super().__init__(
            settings.dummyjson_api_base_url, 
            settings.dummyjson_timeout,
        )

    async def get_user(self, user_id: int) -> DummyUserResponse | None:
        data = await self._make_request(f"/users/{user_id}")
        
        if not data:
            return None
        
        return DummyUserResponse(**data)
    
    async def search_user(self, name: str) -> DummyUserSearchResponse | None:
        data = await self._make_request(f"/users?search={name}")
        
        if not data:
            return None

        return DummyUserSearchResponse(**data)
