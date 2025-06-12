from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Literal

# Shared base schema
class BookingBase(BaseModel):
    service_id: UUID
    start_time: datetime
    end_time: datetime

# For customers creating bookings
class BookingCreate(BookingBase):
    provider_id: UUID

# For reading bookings
class BookingRead(BookingBase):
    id: UUID
    customer_id: UUID
    provider_id: UUID
    status: Literal["confirmed", "cancelled", "pending"]
    created_at: datetime

    class Config:
        from_attributes = True
