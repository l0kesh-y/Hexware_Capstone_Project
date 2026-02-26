import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime

logger = logging.getLogger("audit")


class AuditMiddleware(BaseHTTPMiddleware):
    """Middleware for auditing sensitive operations in healthcare system"""
    
    SENSITIVE_PATHS = [
        "/prescriptions",
        "/appointments",
        "/users/profile",
        "/admin"
    ]
    
    async def dispatch(self, request: Request, call_next):
        # Check if this is a sensitive operation
        is_sensitive = any(path in str(request.url.path) for path in self.SENSITIVE_PATHS)
        
        if is_sensitive and request.method in ["POST", "PUT", "DELETE"]:
            # Extract user info from request state (set by auth dependency)
            user_id = getattr(request.state, "user_id", "anonymous")
            
            # Log audit trail
            logger.info(
                f"AUDIT: {datetime.utcnow().isoformat()} | "
                f"User: {user_id} | "
                f"Action: {request.method} | "
                f"Path: {request.url.path} | "
                f"IP: {request.client.host if request.client else 'unknown'}"
            )
        
        response = await call_next(request)
        return response
