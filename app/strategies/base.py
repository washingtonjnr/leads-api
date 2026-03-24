from abc import ABC, abstractmethod

class BaseStrategy(ABC):
    @abstractmethod
    async def run(self, issue_key: str, summary: str, description: str) -> dict:
        ...
