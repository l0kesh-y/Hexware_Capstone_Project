from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from fastapi import HTTPException, status
from app.models.doctor_profile import DoctorProfile
from app.repositories.doctor_repository import DoctorRepository
from app.schemas.doctor_schema import DoctorProfileCreate, DoctorProfileUpdate


class DoctorService:
    def __init__(self, db: Session):
        self.repository = DoctorRepository(db)
    
    def create_profile(self, user_id: UUID, profile_data: DoctorProfileCreate) -> DoctorProfile:
        # Check if profile already exists
        existing = self.repository.get_by_user_id(user_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Doctor profile already exists"
            )
        
        profile = DoctorProfile(
            user_id=user_id,
            specialization=profile_data.specialization,
            available_from=profile_data.available_from,
            available_to=profile_data.available_to,
            location=profile_data.location
        )
        
        return self.repository.create(profile)
    
    def get_profile(self, user_id: UUID) -> DoctorProfile:
        profile = self.repository.get_by_user_id(user_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Doctor profile not found"
            )
        return profile
    
    def get_all_doctors(self) -> List[DoctorProfile]:
        return self.repository.get_all()
    
    def update_profile(self, user_id: UUID, update_data: DoctorProfileUpdate) -> DoctorProfile:
        profile = self.get_profile(user_id)
        
        if update_data.specialization is not None:
            profile.specialization = update_data.specialization
        if update_data.available_from is not None:
            profile.available_from = update_data.available_from
        if update_data.available_to is not None:
            profile.available_to = update_data.available_to
        if update_data.location is not None:
            profile.location = update_data.location
        
        return self.repository.update(profile)
