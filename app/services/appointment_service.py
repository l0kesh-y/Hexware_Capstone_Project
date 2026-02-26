from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from datetime import datetime
from app.models.appointment import Appointment
from app.repositories.appointment_repository import AppointmentRepository
from app.schemas.appointment_schema import AppointmentCreate, AppointmentUpdate
from app.utils.constants import AppointmentStatus
from fastapi import HTTPException, status


class AppointmentService:
    def __init__(self, db: Session):
        self.repository = AppointmentRepository(db)
    
    def create_appointment(self, patient_id: UUID, appointment_data: AppointmentCreate) -> Appointment:
        appointment = Appointment(
            patient_id=patient_id,
            doctor_id=appointment_data.doctor_id,
            appointment_time=appointment_data.appointment_time,
            notes=appointment_data.notes,
            status=AppointmentStatus.BOOKED
        )
        return self.repository.create(appointment)
    
    def get_appointment(self, appointment_id: UUID) -> Appointment:
        appointment = self.repository.get_by_id(appointment_id)
        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment not found"
            )
        return appointment
    
    def get_patient_appointments(self, patient_id: UUID) -> List[Appointment]:
        return self.repository.get_by_patient(patient_id)
    
    def update_appointment(self, appointment_id: UUID, patient_id: UUID, update_data: AppointmentUpdate) -> Appointment:
        appointment = self.get_appointment(appointment_id)
        
        if appointment.patient_id != patient_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this appointment"
            )
        
        if update_data.appointment_time:
            appointment.appointment_time = update_data.appointment_time
        if update_data.notes is not None:
            appointment.notes = update_data.notes
        
        return self.repository.update(appointment)
    
    def cancel_appointment(self, appointment_id: UUID, patient_id: UUID) -> Appointment:
        appointment = self.get_appointment(appointment_id)
        
        if appointment.patient_id != patient_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to cancel this appointment"
            )
        
        appointment.status = AppointmentStatus.CANCELLED
        return self.repository.update(appointment)
