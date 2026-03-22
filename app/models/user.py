from pydantic import Field, EmailStr

from app.models.base import BaseModel

class User(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    hashed_password: str = Field(..., min_length=10)
    
    is_active: bool = True