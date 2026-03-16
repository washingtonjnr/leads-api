from abc import ABC, abstractmethod
from typing import Any
import httpx
from datetime import datetime

class BaseProvider(ABC):
    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url
        self.timeout = timeout

    @abstractmethod
    async def get_user(self, user_id: int) -> datetime | None:
        pass

    async def _make_request(self, endpoint: str) -> dict[str, Any] | None:
        try:
            url = f"{self.base_url}{endpoint}"
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url)
                
                response.raise_for_status()
                
                return response.json()
        except Exception as e:
            print(f"Unexpected error: {e}")
            
        return None