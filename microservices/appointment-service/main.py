from fastapi import FastAPI, Depends, HTTPException, status, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.dialects.postgresql import UUID
from pydantic import BaseModel
from datetime import datetime
import uuid
import os
import requests

# Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/healthcare")
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth-service:8001")

# Database setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True))
    doctor_id = Column(UUID(as_uuid=True))
    appointment_time = Column(DateTime)
    status = Column(String, default="booked")
    notes = Column(String)

Base.metadata.create_all(bind=engine)

# Schemas
class AppointmentCreate(BaseModel):
    doctor_id: str
    appointment_time: datetime
    notes: str = None

class AppointmentResponse(BaseModel):
    id: str
    patient_id: str
    doctor_id: str
    appointment_time: datetime
    status: str
    notes: str = None
    
    class Config:
        from_attributes = True

# FastAPI app
app = FastAPI(title="Appointment Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Auth validation
def validate_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    
    token = authorization.split(" ")[1]
    try:
        response = requests.post(
            f"{AUTH_SERVICE_URL}/auth/validate-token",
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid token")
        return response.json()
    except Exception:
        raise HTTPException(status_code=401, detail="Auth service unavailable")


# Endpoints
@app.post("/appointments", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
def create_appointment(
    appointment_data: AppointmentCreate,
    db: Session = Depends(get_db),
    user_data: dict = Depends(validate_token)
):
    if user_data.get("role") != "patient":
        raise HTTPException(status_code=403, detail="Only patients can book appointments")
    
    appointment = Appointment(
        patient_id=uuid.UUID(user_data["user_id"]),
        doctor_id=uuid.UUID(appointment_data.doctor_id),
        appointment_time=appointment_data.appointment_time,
        notes=appointment_data.notes,
        status="booked"
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    
    return AppointmentResponse(
        id=str(appointment.id),
        patient_id=str(appointment.patient_id),
        doctor_id=str(appointment.doctor_id),
        appointment_time=appointment.appointment_time,
        status=appointment.status,
        notes=appointment.notes
    )

@app.get("/appointments")
def get_appointments(
    db: Session = Depends(get_db),
    user_data: dict = Depends(validate_token)
):
    if user_data.get("role") == "patient":
        appointments = db.query(Appointment).filter(
            Appointment.patient_id == uuid.UUID(user_data["user_id"])
        ).all()
    elif user_data.get("role") == "doctor":
        appointments = db.query(Appointment).filter(
            Appointment.doctor_id == uuid.UUID(user_data["user_id"])
        ).all()
    else:
        appointments = []
    
    return [
        AppointmentResponse(
            id=str(a.id),
            patient_id=str(a.patient_id),
            doctor_id=str(a.doctor_id),
            appointment_time=a.appointment_time,
            status=a.status,
            notes=a.notes
        ) for a in appointments
    ]

@app.get("/health")
def health():
    return {"status": "healthy", "service": "appointment"}
