from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import timedelta
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schema import UserRegister, UserLogin, Token
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.config import settings


class AuthService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)
    
    def register_user(self, user_data: UserRegister) -> User:
        # Check if user already exists
        existing_user = self.repository.get_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        user = User(
            email=user_data.email,
            password_hash=get_password_hash(user_data.password),
            role=user_data.role,
            first_name=user_data.first_name,
            last_name=user_data.last_name
        )
        
        return self.repository.create(user)
    
    def authenticate_user(self, login_data: UserLogin) -> Token:
        user = self.repository.get_by_email(login_data.email)
        
        if not user or not verify_password(login_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id), "role": user.role.value},
            expires_delta=access_token_expires
        )
        
        return Token(access_token=access_token, token_type="bearer")
