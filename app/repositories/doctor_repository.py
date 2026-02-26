from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from app.models.doctor_profile import DoctorProfile


class DoctorRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, profile: DoctorProfile) -> DoctorProfile:
        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)
        return profile
    
    def get_by_user_id(self, user_id: UUID) -> Optional[DoctorProfile]:
        return self.db.query(DoctorProfile).filter(DoctorProfile.user_id == user_id).first()
    
    def get_all(self) -> List[DoctorProfile]:
        return self.db.query(DoctorProfile).all()
    
    def update(self, profile: DoctorProfile) -> DoctorProfile:
        self.db.commit()
        self.db.refresh(profile)
        return profile
