from pydantic import BaseModel
from uuid import UUID
from datetime import time
from typing import Optional

# Shared base schema
class AvailabilityBase(BaseModel):
    day_of_week: int  # 0 = Sunday, 6 = Saturday
    start_time: time
    end_time: time

# For creating availability entries
class AvailabilityCreate(AvailabilityBase):
    pass

# For reading availability entries
class AvailabilityRead(AvailabilityBase):
    id: UUID
    provider_id: UUID

    class Config:
        from_attributes = True
