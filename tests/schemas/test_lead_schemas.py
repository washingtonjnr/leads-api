from datetime import date
import pytest
from pydantic import ValidationError

from app.schemas.lead.lead_request import LeadCreateSchema, LeadUpdateSchema
from app.schemas.lead.lead_response import LeadResponse
from app.schemas.pagination_response import PaginatedResponse

class TestLeadCreateSchema:
    def test_valid_lead_create_schema(self, valid_lead_create_schema):
        assert valid_lead_create_schema.name == "John Doe"
        assert valid_lead_create_schema.email == "john@example.com"
        assert valid_lead_create_schema.phone == "11999999999"
    
    def test_invalid_name_empty(self):
        with pytest.raises(ValidationError) as exc_info:
            LeadCreateSchema(
                name="",
                email="john@example.com",
                phone="11999999999"
            )
        assert "at least 1 character" in str(exc_info.value).lower()
    
    def test_invalid_email_format(self):
        with pytest.raises(ValidationError):
            LeadCreateSchema(
                name="John Doe",
                email="invalid-email",
                phone="11999999999"
            )
    
    def test_invalid_phone_too_short(self):
        with pytest.raises(ValidationError):
            LeadCreateSchema(
                name="John Doe",
                email="john@example.com",
                phone="119999"
            )
    
    def test_missing_required_fields(self):
        with pytest.raises(ValidationError):
            LeadCreateSchema(name="John Doe")

class TestLeadUpdateSchema:
    def test_valid_lead_update_schema(self, valid_lead_update_schema):
        assert valid_lead_update_schema.name == "John Doe Updated"
        assert valid_lead_update_schema.email == "john.updated@example.com"
        assert valid_lead_update_schema.phone == "11888888888"
        assert valid_lead_update_schema.birth_date == date(1990, 5, 15)
    
    def test_optional_birth_date(self):
        schema = LeadUpdateSchema(
            name="John Doe",
            email="john@example.com",
            phone="11999999999"
        )
        assert schema.birth_date is None
    
    def test_update_schema_inherits_from_create_schema(self):
        schema = LeadUpdateSchema(
            name="John",
            email="john@example.com",
            phone="11999999999",
            birth_date="1990-05-15"
        )
        assert hasattr(schema, "name")
        assert hasattr(schema, "email")
        assert hasattr(schema, "phone")
        assert hasattr(schema, "birth_date")

class TestLeadResponse:
    def test_to_response_basic(self, mock_lead):
        response = LeadResponse.to_response(mock_lead)
        
        assert response.id == "a1b2c3d4-e5f6-4789-0abc-def123456789"
        assert response.name == "John Doe"
        assert response.email == "john@example.com"
        assert response.phone == "11999999999"
        assert response.birth_date is None
    
    def test_to_response_with_birth_date(self, mock_lead_with_birthdate):
        response = LeadResponse.to_response(mock_lead_with_birthdate)
        
        assert response.id == "b2c3d4e5-f6a7-4890-1bcd-ef2345678901"
        assert response.name == "Jane Doe"
        assert response.birth_date == "15/05/1990"
    
    def test_response_validation(self, mock_lead):
        response = LeadResponse.to_response(mock_lead)
        
        assert isinstance(response.name, str)
        assert len(response.name) >= 1
        assert "@" in response.email
        assert len(response.phone) >= 10

class TestPaginatedResponse:
    def test_valid_paginated_response(self):
        response = PaginatedResponse(
            items=[],
            total=100,
            page=1,
            size=10,
            total_pages=10
        )
        assert response.total == 100
        assert response.page == 1
        assert response.size == 10
        assert response.total_pages == 10
    
    def test_paginated_response_with_items(self):
        items = [
            LeadResponse(
                id="uuid1",
                name="John",
                email="john@example.com",
                phone="11999999999"
            )
        ]
        response = PaginatedResponse(
            items=items,
            total=1,
            page=1,
            size=10,
            total_pages=1
        )
        assert len(response.items) == 1
        assert response.items[0].name == "John"
    
    def test_invalid_page_zero(self):
        with pytest.raises(ValidationError):
            PaginatedResponse(
                items=[],
                total=0,
                page=0,
                size=10,
                total_pages=0
            )
    
    def test_invalid_size_zero(self):
        with pytest.raises(ValidationError):
            PaginatedResponse(
                items=[],
                total=0,
                page=1,
                size=0,
                total_pages=0
            )
