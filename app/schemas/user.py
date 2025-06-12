from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    provider = "provider"
    customer = "customer"

# Shared properties
class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: UserRole

# Input schema for user creation
class UserCreate(UserBase):
    password: str

# Schema for reading a user (e.g., in response)
class UserRead(UserBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

