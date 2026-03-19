from pydantic import BaseModel, Field

class TokenResponse(BaseModel):
    access_token: str = Field(..., description="Access token")
    refresh_token: str | None  = Field(None, description="Refresh token")
