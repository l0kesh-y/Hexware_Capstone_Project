from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.user import User
from app.models.appointment import Appointment
from app.models.prescription import Prescription
from app.utils.constants import UserRole, AppointmentStatus


class AdminService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_analytics(self) -> dict:
        # Count users by role
        total_patients = self.db.query(User).filter(User.role == UserRole.PATIENT).count()
        total_doctors = self.db.query(User).filter(User.role == UserRole.DOCTOR).count()
        total_admins = self.db.query(User).filter(User.role == UserRole.ADMIN).count()
        
        # Count appointments by status
        total_appointments = self.db.query(Appointment).count()
        booked_appointments = self.db.query(Appointment).filter(
            Appointment.status == AppointmentStatus.BOOKED
        ).count()
        completed_appointments = self.db.query(Appointment).filter(
            Appointment.status == AppointmentStatus.COMPLETED
        ).count()
        cancelled_appointments = self.db.query(Appointment).filter(
            Appointment.status == AppointmentStatus.CANCELLED
        ).count()
        
        # Count prescriptions
        total_prescriptions = self.db.query(Prescription).count()
        
        return {
            "users": {
                "total_patients": total_patients,
                "total_doctors": total_doctors,
                "total_admins": total_admins,
                "total_users": total_patients + total_doctors + total_admins
            },
            "appointments": {
                "total_appointments": total_appointments,
                "booked": booked_appointments,
                "completed": completed_appointments,
                "cancelled": cancelled_appointments
            },
            "prescriptions": {
                "total_prescriptions": total_prescriptions
            }
        }
