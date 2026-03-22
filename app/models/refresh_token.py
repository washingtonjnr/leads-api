from pydantic import Field
from datetime import datetime, timezone

from app.models.base import BaseModel

class RefreshTokenModel(BaseModel):
    token: str = Field(...)
    user_id: str = Field(...)
    
    revoked: bool = False
    
    expires_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True