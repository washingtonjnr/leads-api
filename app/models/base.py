from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field 


class BaseModel(BaseModel):
    id: Optional[int] = Field(default=None, alias="_id", description="ID numerico interno")
    external_id: str = Field(default_factory=lambda: str(uuid4()), description="UUID público")
   
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )