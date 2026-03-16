import pytest

from unittest.mock import AsyncMock
from app.schemas.lead.lead_response import LeadResponse

class TestLeadsController:
    def test_list_leads(self, client, lead_service, mock_lead):
        lead = LeadResponse.to_response(mock_lead)
        lead_service.get_paginated = AsyncMock(
            return_value={
                "items": [lead],
                "total": 1,
                "page": 1,
                "size": 10,
                "total_pages": 10
            }
        )

        response = client.get("/leads?page=1&size=10")

        assert response.status_code == 200

        body = response.json()
    
        lead_service.get_paginated.assert_called_once_with(page=1, size=10)

        assert "items" in body
        assert body["page"] == 1
        assert body["size"] == 10
        assert body["items"][0]["id"] == lead.id

    def test_list_leads_invalid_page(self, client):
        response = client.get("/leads?page=-1")

        assert response.status_code == 422

        body = response.json()

        assert body["detail"][0]["loc"][-1] == "page"

    def test_list_leads_invalid_size(self, client):
        response = client.get("/leads?size=0")

        assert response.status_code == 422

    def test_get_lead_by_id(self, client, mock_lead, lead_service):
        lead = LeadResponse.to_response(mock_lead)
        external_id = lead.id

        lead_service.get_by_external_id = AsyncMock(return_value=lead)

        response = client.get(f"/leads/{external_id}")
        
        assert response.status_code == 200
    
    def test_get_lead_invalid_id(self, client_no_mock):
        response = client_no_mock.get("/leads/invalid-id")
        
        assert response.status_code in [422, 404]

    def test_create_lead(self, client, lead_service, valid_lead_create_schema):
        schema = valid_lead_create_schema
        
        mock_response = {
            "id": "a1b2c3d4-e5f6-4789-0abc-def123456789",
            "name": schema.name,
            "email": schema.email,
            "phone": schema.phone,
        }
        
        lead_service.create = AsyncMock(return_value=mock_response)

        response = client.post(
            "/leads",
            json=schema.model_dump()
        )

        assert response.status_code == 201

        body = response.json()
        assert body["name"] == "John Doe"
        
        lead_service.create.assert_called_once()

    def test_create_lead_invalid_email(self, client):
        response = client.post(
            "/leads",
            json={
                "name": "John Doe",
                "email": "invalid-email",
                "phone": "11999999999"
            }
        )

        assert response.status_code == 422

    def test_create_lead_missing_fields(self, client):
        response = client.post("/leads", json={})

        assert response.status_code == 422
        