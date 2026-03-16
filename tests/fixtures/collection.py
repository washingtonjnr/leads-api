import pytest
from unittest.mock import AsyncMock

@pytest.fixture
def mock_collection():
    collection = AsyncMock()

    return collection
