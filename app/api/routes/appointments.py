from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.core.database import get_db
from app.core.dependencies import get_current_user, get_current_patient
from app.models.user import User
from app.schemas.appointment_schema import AppointmentCreate, AppointmentUpdate, AppointmentResponse
from app.services.appointment_service import AppointmentService

router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.post("/", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
def create_appointment(
    appointment_data: AppointmentCreate,
    current_user: User = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    """Book a new appointment (Patient only)"""
    service = AppointmentService(db)
    appointment = service.create_appointment(current_user.id, appointment_data)
    return appointment


@router.get("/", response_model=List[AppointmentResponse])
def get_appointments(
    current_user: User = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    """Get all appointments for the current patient"""
    service = AppointmentService(db)
    appointments = service.get_patient_appointments(current_user.id)
    return appointments



@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_appointment(
    appointment_id: UUID,
    current_user: User = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    """Get a specific appointment by ID"""
    service = AppointmentService(db)
    appointment = service.get_appointment(appointment_id)
    return appointment


@router.put("/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(
    appointment_id: UUID,
    update_data: AppointmentUpdate,
    current_user: User = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    """Update an appointment (reschedule)"""
    service = AppointmentService(db)
    appointment = service.update_appointment(appointment_id, current_user.id, update_data)
    return appointment


@router.delete("/{appointment_id}", response_model=AppointmentResponse)
def cancel_appointment(
    appointment_id: UUID,
    current_user: User = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    """Cancel an appointment"""
    service = AppointmentService(db)
    appointment = service.cancel_appointment(appointment_id, current_user.id)
    return appointment
