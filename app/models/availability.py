from sqlalchemy import Column, Integer, Time, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db.base import Base

class Availability(Base):
    __tablename__ = "availability"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    provider_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    day_of_week = Column(Integer, nullable=False)  # 0 = Sunday, 6 = Saturday
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
