from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.dependencies import get_current_doctor
from app.models.user import User
from app.schemas.doctor_schema import DoctorProfileCreate, DoctorProfileUpdate, DoctorProfileResponse
from app.services.doctor_service import DoctorService

router = APIRouter(prefix="/doctors", tags=["Doctors"])


@router.post("/profile", response_model=DoctorProfileResponse, status_code=status.HTTP_201_CREATED)
def create_doctor_profile(
    profile_data: DoctorProfileCreate,
    current_user: User = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """Create doctor profile (Doctor only)"""
    service = DoctorService(db)
    profile = service.create_profile(current_user.id, profile_data)
    return profile


@router.get("/profile", response_model=DoctorProfileResponse)
def get_doctor_profile(
    current_user: User = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """Get current doctor's profile"""
    service = DoctorService(db)
    profile = service.get_profile(current_user.id)
    return profile


@router.put("/profile", response_model=DoctorProfileResponse)
def update_doctor_profile(
    update_data: DoctorProfileUpdate,
    current_user: User = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """Update doctor profile"""
    service = DoctorService(db)
    profile = service.update_profile(current_user.id, update_data)
    return profile


@router.get("/", response_model=List[DoctorProfileResponse])
def get_all_doctors(db: Session = Depends(get_db)):
    """Get all doctors (public endpoint for patients to search)"""
    service = DoctorService(db)
    doctors = service.get_all_doctors()
    return doctors
