from sqlalchemy import Column, String, Time, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class DoctorProfile(BaseModel):
    __tablename__ = "doctor_profiles"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True)
    specialization = Column(String, nullable=False)
    available_from = Column(Time, nullable=True)
    available_to = Column(Time, nullable=True)
    location = Column(String, nullable=True)
    
    user = relationship("User", backref="doctor_profile")
