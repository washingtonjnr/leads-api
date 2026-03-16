from pydantic import BaseModel, Field
from typing import Optional
from app.utils.date import format_date

class LeadResponse(BaseModel):
    id: str = Field(..., description="Lead UUID")
    name: str = Field(..., min_length=1, description="Lead name")
    email: str = Field(..., description="Lead email")
    phone: str = Field(..., description="Lead phone")
    birth_date: Optional[str] = Field(None, description="Lead birth date")

    @classmethod
    def to_response(cls, doc: dict) -> "LeadResponse":
        birth_date = doc.get("birth_date", None)
        
        if birth_date and isinstance(birth_date, str):
            birth_date = format_date(birth_date) 
            
        return cls(
            id=doc.get("external_id", ""),
            name=doc.get("name", ""),
            email=doc.get("email", ""),
            phone=doc.get("phone", ""),
            birth_date=birth_date,
        )