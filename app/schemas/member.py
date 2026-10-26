from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

EMAIL_REGEX = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

class MemberRegisterRequest(BaseModel):
    email: str = Field(..., pattern=EMAIL_REGEX)
    full_name: str = Field(..., min_length=2, max_length=150)
    phone_number: str = Field(..., pattern=r"^\+?[0-9]{10,15}$")
    password: str = Field(..., min_length=6)
    role: Optional[str] = "member"

class MemberLoginRequest(BaseModel):
    email: str = Field(..., pattern=EMAIL_REGEX)
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    email: str
    member_id: int

class MemberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    full_name: str
    phone_number: str
    role: str
    created_at: datetime
