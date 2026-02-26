from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
import logging
from app.core.database import engine, Base
from app.core.config import settings
from app.api.routes import appointments, auth, users, prescriptions, doctors, admin
from app.middleware.logging_middleware import LoggingMiddleware
from app.middleware.audit_middleware import AuditMiddleware
from app.exceptions.exception_handlers import (
    validation_exception_handler,
    sqlalchemy_exception_handler,
    general_exception_handler
)

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Healthcare Appointment & E-Prescription API",
    description="RESTful API for managing healthcare appointments and e-prescriptions",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(AuditMiddleware)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
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
    return {
        "message": "Healthcare API - Sprint 4: Security & Deployment",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0"
    }
