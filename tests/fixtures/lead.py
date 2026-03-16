import pytest
from unittest.mock import AsyncMock

from app.schemas.lead.lead_request import LeadCreateSchema, LeadUpdateSchema
from app.services.lead import LeadService
from app.repositories.lead import LeadRepository
from app.providers.dummyjson import DummyJSONProvider

# PROVIDER
@pytest.fixture
def dummy_provider():
    provider = AsyncMock(spec=DummyJSONProvider)
    return provider


# REPOSITORY
@pytest.fixture
def lead_repository(mock_db):
    return LeadRepository(mock_db)


# SERVICE
@pytest.fixture
def lead_service(lead_repository, dummy_provider):
    service = LeadService(
        repository=lead_repository,
        dummy_provider=dummy_provider
    )
    return service


# MODELS
@pytest.fixture
def mock_lead():
    return {
        "_id": 1,
        "external_id": "a1b2c3d4-e5f6-4789-0abc-def123456789",
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "11999999999",
        "birth_date": None
    }

@pytest.fixture
def mock_lead_with_birthdate():
    return {
        "_id": 2,
        "external_id": "b2c3d4e5-f6a7-4890-1bcd-ef2345678901",
        "name": "Jane Doe",
        "email": "jane@example.com",
        "phone": "11988888888",
        "birth_date": "1990-05-15"
    }


# SCHEMAS
@pytest.fixture
def valid_lead_create_schema():
    return LeadCreateSchema(
        name="John Doe",
        email="john@example.com",
        phone="11999999999"
    )

@pytest.fixture
def valid_lead_update_schema():
    return LeadUpdateSchema(
        name="John Doe Updated",
        email="john.updated@example.com",
        phone="11888888888",
        birth_date="1990-05-15"
    )
