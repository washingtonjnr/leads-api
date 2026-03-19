from pydantic import BaseModel, Field, EmailStr

class UserResponse(BaseModel):
    id: str = Field(..., description="User UUID")
    name: str = Field(..., min_length=1, description="User name")
    email: EmailStr = Field(..., description="User email")

    @classmethod
    def to_response(cls, doc: dict) -> "UserResponse":
        return cls(
            id=doc.get("external_id", ""),
            name=doc.get("name", ""),
            email=doc.get("email", ""),
        )