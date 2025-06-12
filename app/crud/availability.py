from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.models.availability import Availability
from app.schemas.availability import AvailabilityCreate

def create_availability(db: Session, provider_id: UUID, availability_in: AvailabilityCreate) -> Availability:
    availability = Availability(
        provider_id=provider_id,
        day_of_week=availability_in.day_of_week,
        start_time=availability_in.start_time,
        end_time=availability_in.end_time
    )
    db.add(availability)
    db.commit()
    db.refresh(availability)
    return availability

def get_availability_for_provider(db: Session, provider_id: UUID) -> List[Availability]:
    return db.query(Availability).filter(Availability.provider_id == provider_id).all()

def delete_availability(db: Session, availability_id: UUID) -> None:
    availability = db.query(Availability).filter(Availability.id == availability_id).first()
    if availability:
        db.delete(availability)
        db.commit()
