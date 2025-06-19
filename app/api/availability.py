from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.availability import AvailabilityCreate, AvailabilityRead
from app.crud import availability as availability_crud
from app.models.availability import Availability

router = APIRouter()

@router.post("/availability", response_model=AvailabilityRead)
def create_availability(
    availability_in: AvailabilityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "provider":
        raise HTTPException(status_code=403, detail="Only providers can set availability.")
    return availability_crud.create_availability(db, current_user.id, availability_in)

@router.get("/availability", response_model=List[AvailabilityRead])
def list_provider_availability(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return availability_crud.get_availability_for_provider(db, current_user.id)

@router.get("/availability/by_provider/{provider_id}", response_model=List[AvailabilityRead])
def get_availability_by_provider_id(provider_id: UUID, db: Session = Depends(get_db)):
    return db.query(Availability).filter(Availability.provider_id == provider_id).all()


@router.delete("/availability/{availability_id}")
def delete_availability(
    availability_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    entries = availability_crud.get_availability_for_provider(db, current_user.id)
    if not any(a.id == availability_id for a in entries):
        raise HTTPException(status_code=404, detail="Availability entry not found.")
    availability_crud.delete_availability(db, availability_id)
    return {"detail": "Deleted"}

@router.get("/availability/all", response_model=List[AvailabilityRead])
def get_all_availability(db: Session = Depends(get_db)):
    return db.query(Availability).all()
