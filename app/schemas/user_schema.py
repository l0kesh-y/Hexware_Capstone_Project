from pydantic import BaseModel, EmailStr, UUID4
from typing import Optional
from datetime import datetime
from app.utils.constants import UserRole


class UserResponse(BaseModel):
    id: UUID4
    email: EmailStr
    role: UserRole
    first_name: str
    last_name: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
