from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from app.models.appointment import Appointment
from app.utils.constants import AppointmentStatus
from datetime import datetime


class AppointmentRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, appointment: Appointment) -> Appointment:
        self.db.add(appointment)
        self.db.commit()
        self.db.refresh(appointment)
        return appointment
    
    def get_by_id(self, appointment_id: UUID) -> Optional[Appointment]:
        return self.db.query(Appointment).filter(Appointment.id == appointment_id).first()
    
    def get_by_patient(self, patient_id: UUID) -> List[Appointment]:
        return self.db.query(Appointment).filter(Appointment.patient_id == patient_id).all()
    
    def get_by_doctor(self, doctor_id: UUID) -> List[Appointment]:
        return self.db.query(Appointment).filter(Appointment.doctor_id == doctor_id).all()
    
    def update(self, appointment: Appointment) -> Appointment:
        self.db.commit()
        self.db.refresh(appointment)
        return appointment
    
    def delete(self, appointment: Appointment) -> None:
        self.db.delete(appointment)
        self.db.commit()
