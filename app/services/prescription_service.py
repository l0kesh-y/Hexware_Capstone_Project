from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from fastapi import HTTPException, status
from app.models.prescription import Prescription
from app.models.appointment import Appointment
from app.repositories.prescription_repository import PrescriptionRepository
from app.repositories.appointment_repository import AppointmentRepository
from app.schemas.prescription_schema import PrescriptionCreate, PrescriptionUpdate
from app.utils.constants import AppointmentStatus


class PrescriptionService:
    def __init__(self, db: Session):
        self.repository = PrescriptionRepository(db)
        self.appointment_repository = AppointmentRepository(db)
    
    def create_prescription(self, doctor_id: UUID, prescription_data: PrescriptionCreate) -> Prescription:
        # Verify appointment exists and belongs to the doctor
        appointment = self.appointment_repository.get_by_id(prescription_data.appointment_id)
        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment not found"
            )
        
        if appointment.doctor_id != doctor_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to create prescription for this appointment"
            )
        
        # Check if prescription already exists
        existing = self.repository.get_by_appointment(prescription_data.appointment_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Prescription already exists for this appointment"
            )
        
        # Convert medicines to dict format
        medicines_dict = [med.dict() for med in prescription_data.medicines]
        
        prescription = Prescription(
            appointment_id=prescription_data.appointment_id,
            doctor_id=doctor_id,
            patient_id=appointment.patient_id,
            notes=prescription_data.notes,
            medicines=medicines_dict
        )
        
        # Mark appointment as completed
        appointment.status = AppointmentStatus.COMPLETED
        self.appointment_repository.update(appointment)
        
        return self.repository.create(prescription)
    
    def get_prescription(self, prescription_id: UUID) -> Prescription:
        prescription = self.repository.get_by_id(prescription_id)
        if not prescription:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Prescription not found"
            )
        return prescription
    
    def get_patient_prescriptions(self, patient_id: UUID) -> List[Prescription]:
        return self.repository.get_by_patient(patient_id)
    
    def get_doctor_prescriptions(self, doctor_id: UUID) -> List[Prescription]:
        return self.repository.get_by_doctor(doctor_id)
    
    def update_prescription(self, prescription_id: UUID, doctor_id: UUID, update_data: PrescriptionUpdate) -> Prescription:
        prescription = self.get_prescription(prescription_id)
        
        if prescription.doctor_id != doctor_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this prescription"
            )
        
        if update_data.notes is not None:
            prescription.notes = update_data.notes
        if update_data.medicines is not None:
            prescription.medicines = [med.dict() for med in update_data.medicines]
        
        return self.repository.update(prescription)
