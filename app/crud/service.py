from sqlalchemy.orm import Session
from typing import List
from app.models.service import Service
from app.schemas.service import ServiceCreate
import uuid

def create_service(db: Session, provider_id: uuid.UUID, service_in: ServiceCreate) -> Service:
    service = Service(
        provider_id=provider_id,
        name=service_in.name,
        description=service_in.description,
        duration_minutes=service_in.duration_minutes,
        price_cents=service_in.price_cents
    )
    db.add(service)
    db.commit()
    db.refresh(service)
    return service

def get_services_by_provider(db: Session, provider_id: uuid.UUID) -> List[Service]:
    return db.query(Service).filter(Service.provider_id == provider_id).all()

def get_service(db: Session, service_id: uuid.UUID) -> Service:
    return db.query(Service).filter(Service.id == service_id).first()

def delete_service(db: Session, service_id: uuid.UUID) -> None:
    service = db.query(Service).filter(Service.id == service_id).first()
    if service:
        db.delete(service)
        db.commit()

def update_service(db: Session, service_id: uuid.UUID, updates: dict) -> Service:
    service = db.query(Service).filter(Service.id == service_id).first()
    if service:
        for key, value in updates.items():
            setattr(service, key, value)
        db.commit()
        db.refresh(service)
    return service
