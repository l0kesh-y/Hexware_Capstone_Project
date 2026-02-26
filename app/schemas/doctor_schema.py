from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import time


class DoctorProfileCreate(BaseModel):
    specialization: str
    available_from: Optional[time] = None
    available_to: Optional[time] = None
    location: Optional[str] = None


class DoctorProfileUpdate(BaseModel):
    specialization: Optional[str] = None
    available_from: Optional[time] = None
    available_to: Optional[time] = None
    location: Optional[str] = None


class DoctorProfileResponse(BaseModel):
    id: UUID4
    user_id: UUID4
    specialization: str
    available_from: Optional[time] = None
    available_to: Optional[time] = None
    location: Optional[str] = None
    
    class Config:
        from_attributes = True
