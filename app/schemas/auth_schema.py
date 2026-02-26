from pydantic import BaseModel, EmailStr
from app.utils.constants import UserRole


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    role: UserRole
    first_name: str
    last_name: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: str
    role: UserRole
