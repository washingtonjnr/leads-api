from pydantic import BaseModel, Field, EmailStr

class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., description="User password")

class RefreshRequest(BaseModel):
    refresh_token: str = Field(..., description="Refresh token")
