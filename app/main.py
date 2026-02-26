from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.api.routes import appointments, auth, users, prescriptions, doctors, admin

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Healthcare Appointment & E-Prescription API",
    description="RESTful API for managing healthcare appointments and e-prescriptions",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(appointments.router)
app.include_router(prescriptions.router)
app.include_router(doctors.router)
app.include_router(admin.router)


@app.get("/")
def root():
    return {"message": "Healthcare API - Sprint 3: Prescription & Admin Reporting"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
