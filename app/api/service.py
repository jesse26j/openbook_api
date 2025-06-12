from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app.schemas.service import ServiceCreate, ServiceRead
from app.crud import service as service_crud
from app.api.deps import get_db, get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/services", response_model=ServiceRead)
def create_service(
    service_in: ServiceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "provider":
        raise HTTPException(status_code=403, detail="Only providers can create services.")
    return service_crud.create_service(db, current_user.id, service_in)

@router.get("/services", response_model=List[ServiceRead])
def list_services(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return service_crud.get_services_by_provider(db, current_user.id)

@router.get("/services/{service_id}", response_model=ServiceRead)
def get_service(
    service_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    svc = service_crud.get_service(db, service_id)
    if not svc or svc.provider_id != current_user.id:
        raise HTTPException(status_code=404, detail="Service not found.")
    return svc

@router.delete("/services/{service_id}")
def delete_service(
    service_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    svc = service_crud.get_service(db, service_id)
    if not svc or svc.provider_id != current_user.id:
        raise HTTPException(status_code=404, detail="Service not found.")
    service_crud.delete_service(db, service_id)
    return {"detail": "Deleted"}

# Optional: You can also add a PUT route for updating
