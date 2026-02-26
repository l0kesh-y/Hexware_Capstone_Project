from fastapi import FastAPI, Depends, HTTPException, status, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.dialects.postgresql import UUID
from pydantic import BaseModel
from typing import List
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
class Prescription(Base):
    __tablename__ = "prescriptions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    appointment_id = Column(UUID(as_uuid=True), unique=True)
    doctor_id = Column(UUID(as_uuid=True))
    patient_id = Column(UUID(as_uuid=True))
    notes = Column(String)
    medicines = Column(JSON)

Base.metadata.create_all(bind=engine)

# Schemas
class Medicine(BaseModel):
    name: str
    dosage: str
    duration: str
    instructions: str = None

class PrescriptionCreate(BaseModel):
    appointment_id: str
    notes: str = None
    medicines: List[Medicine]

class PrescriptionResponse(BaseModel):
    id: str
    appointment_id: str
    doctor_id: str
    patient_id: str
    notes: str = None
    medicines: List[dict]
    
    class Config:
        from_attributes = True

# FastAPI app
app = FastAPI(title="Prescription Service", version="1.0.0")

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
@app.post("/prescriptions", response_model=PrescriptionResponse, status_code=status.HTTP_201_CREATED)
def create_prescription(
    prescription_data: PrescriptionCreate,
    db: Session = Depends(get_db),
    user_data: dict = Depends(validate_token)
):
    if user_data.get("role") != "doctor":
        raise HTTPException(status_code=403, detail="Only doctors can create prescriptions")
    
    # Check if prescription already exists
    existing = db.query(Prescription).filter(
        Prescription.appointment_id == uuid.UUID(prescription_data.appointment_id)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Prescription already exists")
    
    medicines_dict = [med.dict() for med in prescription_data.medicines]
    
    prescription = Prescription(
        appointment_id=uuid.UUID(prescription_data.appointment_id),
        doctor_id=uuid.UUID(user_data["user_id"]),
        patient_id=uuid.uuid4(),  # In real app, get from appointment
        notes=prescription_data.notes,
        medicines=medicines_dict
    )
    db.add(prescription)
    db.commit()
    db.refresh(prescription)
    
    return PrescriptionResponse(
        id=str(prescription.id),
        appointment_id=str(prescription.appointment_id),
        doctor_id=str(prescription.doctor_id),
        patient_id=str(prescription.patient_id),
        notes=prescription.notes,
        medicines=prescription.medicines
    )

@app.get("/prescriptions")
def get_prescriptions(
    db: Session = Depends(get_db),
    user_data: dict = Depends(validate_token)
):
    if user_data.get("role") == "patient":
        prescriptions = db.query(Prescription).filter(
            Prescription.patient_id == uuid.UUID(user_data["user_id"])
        ).all()
    elif user_data.get("role") == "doctor":
        prescriptions = db.query(Prescription).filter(
            Prescription.doctor_id == uuid.UUID(user_data["user_id"])
        ).all()
    else:
        prescriptions = []
    
    return [
        PrescriptionResponse(
            id=str(p.id),
            appointment_id=str(p.appointment_id),
            doctor_id=str(p.doctor_id),
            patient_id=str(p.patient_id),
            notes=p.notes,
            medicines=p.medicines
        ) for p in prescriptions
    ]

@app.get("/health")
def health():
    return {"status": "healthy", "service": "prescription"}
