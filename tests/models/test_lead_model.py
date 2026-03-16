import pytest
from pydantic import ValidationError

from app.models.lead import Lead


class TestLeadModel:
    def test_create_valid_lead(self):
        lead = Lead(
            name="John Doe",
            email="john@example.com",
            phone="11999999999"
        )
        assert lead.name == "John Doe"
        assert lead.email == "john@example.com"
        assert lead.phone == "11999999999"
        assert lead.birth_date is None
    
    def test_create_lead_with_birth_date(self):
        lead = Lead(
            name="Jane Doe",
            email="jane@example.com",
            phone="11988888888",
            birth_date="1990-05-15"
        )
        assert lead.birth_date == "1990-05-15"
    
    def test_name_required(self):
        with pytest.raises(ValidationError):
            Lead(
                email="john@example.com",
                phone="11999999999"
            )
    
    def test_name_min_length(self):
        with pytest.raises(ValidationError):
            Lead(
                name="",
                email="john@example.com",
                phone="11999999999"
            )
    
    def test_email_required_and_valid(self):
        with pytest.raises(ValidationError):
            Lead(
                name="John Doe",
                phone="11999999999"
            )
        
        with pytest.raises(ValidationError):
            Lead(
                name="John Doe",
                email="invalid-email",
                phone="11999999999"
            )
    
    def test_phone_required(self):
        with pytest.raises(ValidationError):
            Lead(
                name="John Doe",
                email="john@example.com"
            )
    
    def test_phone_min_length(self):
        with pytest.raises(ValidationError):
            Lead(
                name="John Doe",
                email="john@example.com",
                phone="119"
            )
    
    def test_lead_model_dump(self):
        lead = Lead(
            name="John Doe",
            email="john@example.com",
            phone="11999999999",
            birth_date="1990-05-15"
        )
        data = lead.model_dump()
        
        assert data["name"] == "John Doe"
        assert data["email"] == "john@example.com"
        assert data["phone"] == "11999999999"
        assert data["birth_date"] == "1990-05-15"
    
    def test_lead_model_dump_exclude_none(self):
        lead = Lead(
            name="John Doe",
            email="john@example.com",
            phone="11999999999"
        )
        data = lead.model_dump(exclude_none=True)
        
        assert "birth_date" not in data
        assert data["name"] == "John Doe"
    
    def test_lead_birth_date_optional(self):
        lead = Lead(
            name="John Doe",
            email="john@example.com",
            phone="11999999999"
        )
        assert lead.birth_date is None
    
    def test_lead_from_dict(self, mock_lead):
        lead = Lead(**mock_lead)
        
        assert lead.name == "John Doe"
        assert lead.email == "john@example.com"
        assert lead.phone == "11999999999"
