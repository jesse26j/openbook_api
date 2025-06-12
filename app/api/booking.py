from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.schemas.booking import BookingCreate, BookingRead
from app.crud import booking as booking_crud
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.booking import Booking, BookingStatus

router = APIRouter()

@router.post("/bookings", response_model=BookingRead)
def create_booking(
    booking_in: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "customer":
        raise HTTPException(status_code=403, detail="Only customers can book services.")

    overlaps = booking_crud.get_overlapping_bookings(
        db,
        provider_id=booking_in.provider_id,
        start_time=booking_in.start_time,
        end_time=booking_in.end_time,
    )
    if overlaps:
        raise HTTPException(status_code=409, detail="Time slot is already booked.")

    return booking_crud.create_booking(db, current_user.id, booking_in)

@router.get("/bookings", response_model=List[BookingRead])
def get_my_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return booking_crud.get_bookings_for_user(db, current_user.id)

@router.patch("/bookings/{booking_id}/cancel", response_model=BookingRead)
def cancel_booking(
    booking_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if current_user.id not in [booking.customer_id, booking.provider_id]:
        raise HTTPException(status_code=403, detail="Not authorized to cancel this booking")

    booking.status = "cancelled"
    db.commit()
    db.refresh(booking)
    return booking

@router.patch("/bookings/{booking_id}", response_model=BookingRead)
def update_booking_status(
    booking_id: UUID,
    new_status: BookingStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if current_user.id != booking.provider_id:
        raise HTTPException(status_code=403, detail="Only the provider can update booking status")

    booking.status = new_status
    db.commit()
    db.refresh(booking)
    return booking

from datetime import datetime

@router.patch("/bookings/{booking_id}/reschedule", response_model=BookingRead)
def reschedule_booking(
    booking_id: UUID,
    new_start_time: datetime,
    new_end_time: datetime,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if current_user.id != booking.customer_id:
        raise HTTPException(status_code=403, detail="Only the customer can reschedule this booking")

    # Prevent overlapping bookings
    overlaps = booking_crud.get_overlapping_bookings(
        db,
        provider_id=booking.provider_id,
        start_time=new_start_time,
        end_time=new_end_time
    )
    if overlaps and booking.id not in [b.id for b in overlaps]:
        raise HTTPException(status_code=409, detail="New time overlaps with another booking")

    booking.start_time = new_start_time
    booking.end_time = new_end_time
    booking.status = "pending"  # optional reset
    db.commit()
    db.refresh(booking)
    return booking

@router.patch("/bookings/{booking_id}/reschedule", response_model=BookingRead)
def reschedule_booking(
    booking_id: UUID,
    new_start_time: datetime = Body(...),
    new_end_time: datetime = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if current_user.id != booking.customer_id:
        raise HTTPException(status_code=403, detail="Only the customer can reschedule this booking")

    # Check for conflicts
    overlaps = booking_crud.get_overlapping_bookings(
        db,
        provider_id=booking.provider_id,
        start_time=new_start_time,
        end_time=new_end_time
    )
    if any(b.id != booking.id for b in overlaps):
        raise HTTPException(status_code=409, detail="New time slot is already booked")

    booking.start_time = new_start_time
    booking.end_time = new_end_time
    booking.status = "pending"  # Optional: reset status on change
    db.commit()
    db.refresh(booking)
    return booking