from pydantic import BaseModel, UUID4
from typing import List, Optional
from datetime import datetime


class Medicine(BaseModel):
    name: str
    dosage: str
    duration: str
    instructions: Optional[str] = None


class PrescriptionCreate(BaseModel):
    appointment_id: UUID4
    notes: Optional[str] = None
    medicines: List[Medicine]


class PrescriptionUpdate(BaseModel):
    notes: Optional[str] = None
    medicines: Optional[List[Medicine]] = None


class PrescriptionResponse(BaseModel):
    id: UUID4
    appointment_id: UUID4
    doctor_id: UUID4
    patient_id: UUID4
    notes: Optional[str] = None
    medicines: List[dict]
    created_at: datetime
    
    class Config:
        from_attributes = True
