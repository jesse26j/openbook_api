from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List
from uuid import UUID
from datetime import datetime

from app.models.booking import Booking
from app.schemas.booking import BookingCreate

def create_booking(db: Session, customer_id: UUID, booking_in: BookingCreate) -> Booking:
    booking = Booking(
        customer_id=customer_id,
        provider_id=booking_in.provider_id,
        service_id=booking_in.service_id,
        start_time=booking_in.start_time,
        end_time=booking_in.end_time,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

def get_bookings_for_user(db: Session, user_id: UUID) -> List[Booking]:
    return db.query(Booking).filter(
        (Booking.customer_id == user_id) | (Booking.provider_id == user_id)
    ).order_by(Booking.start_time).all()

def get_overlapping_bookings(
    db: Session, provider_id: UUID, start_time: datetime, end_time: datetime
) -> List[Booking]:
    return db.query(Booking).filter(
        Booking.provider_id == provider_id,
        Booking.start_time < end_time,
        Booking.end_time > start_time,
        Booking.status == "confirmed"
    ).all()
