from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import Optional
from app.utils.constants import AppointmentStatus


class AppointmentCreate(BaseModel):
    doctor_id: UUID4
    appointment_time: datetime
    notes: Optional[str] = None


class AppointmentUpdate(BaseModel):
    appointment_time: Optional[datetime] = None
    notes: Optional[str] = None


class AppointmentResponse(BaseModel):
    id: UUID4
    patient_id: UUID4
    doctor_id: UUID4
    appointment_time: datetime
    status: AppointmentStatus
    notes: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
