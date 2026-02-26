from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_admin
from app.models.user import User
from app.services.admin_service import AdminService

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/analytics")
def get_analytics(
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get system analytics and reports (Admin only)"""
    service = AdminService(db)
    analytics = service.get_analytics()
    return analytics
