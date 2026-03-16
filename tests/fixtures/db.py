import pytest
from unittest.mock import AsyncMock
from motor.motor_asyncio import AsyncIOMotorDatabase

@pytest.fixture
def mock_db():
    db = AsyncMock(spec=AsyncIOMotorDatabase)
    
    return db
