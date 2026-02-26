from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.core.database import get_db
from app.core.dependencies import get_current_user, get_current_doctor, get_current_patient
from app.models.user import User
from app.schemas.prescription_schema import PrescriptionCreate, PrescriptionUpdate, PrescriptionResponse
from app.services.prescription_service import PrescriptionService

router = APIRouter(prefix="/prescriptions", tags=["Prescriptions"])


@router.post("/", response_model=PrescriptionResponse, status_code=status.HTTP_201_CREATED)
def create_prescription(
    prescription_data: PrescriptionCreate,
    current_user: User = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """Create a new prescription (Doctor only)"""
    service = PrescriptionService(db)
    prescription = service.create_prescription(current_user.id, prescription_data)
    return prescription


@router.get("/", response_model=List[PrescriptionResponse])
def get_prescriptions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get prescriptions (patients see their own, doctors see their issued prescriptions)"""
    service = PrescriptionService(db)
    
    if current_user.role.value == "patient":
        prescriptions = service.get_patient_prescriptions(current_user.id)
    elif current_user.role.value == "doctor":
        prescriptions = service.get_doctor_prescriptions(current_user.id)
    else:
        prescriptions = []
    
    return prescriptions



@router.get("/{prescription_id}", response_model=PrescriptionResponse)
def get_prescription(
    prescription_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific prescription by ID"""
    service = PrescriptionService(db)
    prescription = service.get_prescription(prescription_id)
    
    # Verify user has access to this prescription
    if current_user.role.value == "patient" and prescription.patient_id != current_user.id:
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Not authorized")
    elif current_user.role.value == "doctor" and prescription.doctor_id != current_user.id:
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return prescription


@router.put("/{prescription_id}", response_model=PrescriptionResponse)
def update_prescription(
    prescription_id: UUID,
    update_data: PrescriptionUpdate,
    current_user: User = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """Update a prescription (Doctor only)"""
    service = PrescriptionService(db)
    prescription = service.update_prescription(prescription_id, current_user.id, update_data)
    return prescription
