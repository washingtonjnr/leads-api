from abc import ABC, abstractmethod

class BaseAgent(ABC):
    @abstractmethod
    async def build_task(self, prompt: str) -> dict:
        ...