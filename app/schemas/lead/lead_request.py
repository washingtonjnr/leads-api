from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, EmailStr

class LeadCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, description="Lead name")
    email: EmailStr = Field(..., description="Lead email")
    phone: str = Field(..., min_length=10, description="Lead phone")

class LeadUpdateSchema(LeadCreateSchema):
    birth_date: Optional[date] = Field(None, description="Lead birth date")