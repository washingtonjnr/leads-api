from pydantic import BaseModel, Field, EmailStr

class UserBase(BaseModel):
    name: str = Field(..., min_length=1, description="User name")
    email: EmailStr = Field(..., description="User email")

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)