from datetime import date
from typing import Optional

from pydantic import Field, EmailStr

from app.models.base import BaseModel

class Lead(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    phone: str = Field(..., min_length=10)

    birth_date: Optional[str] = None