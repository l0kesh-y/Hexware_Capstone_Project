from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from app.models.prescription import Prescription


class PrescriptionRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, prescription: Prescription) -> Prescription:
        self.db.add(prescription)
        self.db.commit()
        self.db.refresh(prescription)
        return prescription
    
    def get_by_id(self, prescription_id: UUID) -> Optional[Prescription]:
        return self.db.query(Prescription).filter(Prescription.id == prescription_id).first()
    
    def get_by_appointment(self, appointment_id: UUID) -> Optional[Prescription]:
        return self.db.query(Prescription).filter(Prescription.appointment_id == appointment_id).first()
    
    def get_by_patient(self, patient_id: UUID) -> List[Prescription]:
        return self.db.query(Prescription).filter(Prescription.patient_id == patient_id).all()
    
    def get_by_doctor(self, doctor_id: UUID) -> List[Prescription]:
        return self.db.query(Prescription).filter(Prescription.doctor_id == doctor_id).all()
    
    def update(self, prescription: Prescription) -> Prescription:
        self.db.commit()
        self.db.refresh(prescription)
        return prescription
