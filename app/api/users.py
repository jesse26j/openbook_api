from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.user import User
from app.schemas.user import UserRead

router = APIRouter()

@router.get("/providers", response_model=list[UserRead])
def get_all_providers(search: str = Query(None), db: Session = Depends(get_db)):
    query = db.query(User).filter(User.role == "provider")
    if search:
        query = query.filter(User.name.ilike(f"%{search}%"))
    return query.all()
