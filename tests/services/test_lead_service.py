import pytest

from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException

from app.models.lead import Lead
from app.schemas.lead.lead_request import LeadCreateSchema

class TestLeadService:
    async def test_get_all(self, lead_service, mock_lead, mock_lead_with_birthdate):
        leads = [
            Lead(**mock_lead),
            Lead(**mock_lead_with_birthdate)
        ]
        lead_service.repository.find_all = AsyncMock(return_value=leads)
        
        result = await lead_service.get_all()
        
        assert len(result) == 2
        assert result[0].email == "john@example.com"
        assert result[1].email == "jane@example.com"
    
    async def test_get_all_empty(self, lead_service):
        lead_service.repository.find_all = AsyncMock(return_value=[])
        
        result = await lead_service.get_all()
        
        assert len(result) == 0
    
    async def test_get_by_external_id(self, lead_service, mock_lead):
        lead_service.repository.find_by_external_id = AsyncMock(return_value=Lead(**mock_lead))
        
        result = await lead_service.get_by_external_id("a1b2c3d4-e5f6-4789-0abc-def123456789")
        
        lead_service.repository.find_by_external_id.assert_called_once_with(
            "a1b2c3d4-e5f6-4789-0abc-def123456789"
        )
        
        assert result.name == "John Doe"
        assert result.email == "john@example.com"
    
    async def test_get_all_paginated(self, lead_service, mock_lead):
        leads = [Lead(**mock_lead)]
        lead_service.repository.find_paginated = AsyncMock(return_value=(leads, 1))
        
        result = await lead_service.get_paginated(page=1, size=10)
        
        assert len(result.items) == 1
        assert result.total == 1
        assert result.page == 1
        assert result.size == 10
        assert result.total_pages == 1
    
    async def test_get_all_paginated_multiple_pages(self, lead_service, mock_lead):
        leads = [Lead(**mock_lead)]
        lead_service.repository.find_paginated = AsyncMock(return_value=(leads, 100))
        
        result = await lead_service.get_paginated(page=1, size=10)
        
        assert result.total == 100
        assert result.total_pages == 10
    
    async def test_create_lead_success(self, lead_service, valid_lead_create_schema, mock_lead):
        lead_service.repository.get_by_email = AsyncMock(return_value=None)
        
        new_lead = Lead(**mock_lead)
        
        lead_service.repository.create = AsyncMock(return_value=new_lead)
        lead_service.dummy_provider.get_user = AsyncMock(return_value=None)
        
        result = await lead_service.create(valid_lead_create_schema)
        
        assert result.name == "John Doe"
        assert result.email == "john@example.com"
        assert result.birth_date == None
        
        lead_service.repository.create.assert_called_once()
    
    async def test_create_lead_email_already_exists(self, lead_service, valid_lead_create_schema, mock_lead):
        existing_lead = Lead(**mock_lead)
        lead_service.repository.get_by_email = AsyncMock(return_value=existing_lead)
        
        with pytest.raises(HTTPException) as exc_info:
            await lead_service.create(valid_lead_create_schema)
        
        assert exc_info.value.status_code == 400
        assert "already registered" in exc_info.value.detail
    
    async def test_create_lead_with_dummy_json_data(self, lead_service):
        mock_lead_response = {
            "_id": 1,
            "external_id": "uuid-1234",
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "11999999999",
            "birth_date": None
        }

        new_lead = Lead(**mock_lead_response)

        mock_user = MagicMock()
        mock_user.birthDate = "1990-05-15"

        lead_service.repository.get_by_email = AsyncMock(return_value=None)
        lead_service.repository.create = AsyncMock(return_value=new_lead)
        lead_service.repository.update = AsyncMock(return_value=new_lead)

        lead_service.dummy_provider.get_user = AsyncMock(return_value=mock_user)

        data = LeadCreateSchema(
            name="John Doe",
            email="john@example.com",
            phone="11999999999"
        )

        result = await lead_service.create(data)

        lead_service.repository.create.assert_called_once()

        assert result.email == "john@example.com"
    
    async def test_create_lead_without_dummy_json_data(self, lead_service):
        mock_lead_response = {
            "_id": 1,
            "external_id": "uuid-1234",
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "11999999999",
            "birth_date": None
        }

        new_lead = Lead(**mock_lead_response)

        mock_user = MagicMock()
        mock_user.birthDate = "1990-05-15"

        lead_service.repository.get_by_email = AsyncMock(return_value=None)
        lead_service.repository.create = AsyncMock(return_value=new_lead)
        lead_service.repository.update = AsyncMock(return_value=new_lead)

        lead_service.dummy_provider.get_user = AsyncMock(return_value=None)

        data = LeadCreateSchema(
            name="John Doe",
            email="john@example.com",
            phone="11999999999"
        )

        result = await lead_service.create(data)

        lead_service.repository.create.assert_called_once()

        assert result.email == "john@example.com"