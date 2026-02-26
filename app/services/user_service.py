from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import HTTPException, status
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserUpdate


class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)
    
    def get_user_profile(self, user_id: UUID) -> User:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
    
    def update_user_profile(self, user_id: UUID, update_data: UserUpdate) -> User:
        user = self.get_user_profile(user_id)
        
        if update_data.first_name is not None:
            user.first_name = update_data.first_name
        if update_data.last_name is not None:
            user.last_name = update_data.last_name
        if update_data.email is not None:
            # Check if email is already taken
            existing_user = self.repository.get_by_email(update_data.email)
            if existing_user and existing_user.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already in use"
                )
            user.email = update_data.email
        
        return self.repository.update(user)
    
    def get_all_users(self) -> list[User]:
        return self.repository.get_all()
