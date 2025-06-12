from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

# Shared base schema
class ServiceBase(BaseModel):
    name: str
    description: Optional[str] = None
    duration_minutes: int
    price_cents: Optional[int] = None

# For creating a new service
class ServiceCreate(ServiceBase):
    pass

# For reading from DB
class ServiceRead(ServiceBase):
    id: UUID
    provider_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
