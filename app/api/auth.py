from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.user import UserCreate, UserRead, LoginRequest
from app.crud.user import get_user_by_email, create_user, verify_password, get_user_by_username
from app.core.security import create_access_token


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UserRead)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username already taken")
    return create_user(db, user)


@router.post("/login")
def login(form: LoginRequest, db: Session = Depends(get_db)):
    user = (
        db.query(User)
        .filter((User.email == form.login) | (User.username == form.login))
        .first()
    )
    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


from app.api.deps import get_current_user
from app.models.user import User

@router.get("/me", response_model=UserRead)
def read_current_user(current_user: User = Depends(get_current_user)):
    print('HERE!')
    return current_user

@router.get("/providers", response_model=List[UserRead])
def list_providers(db: Session = Depends(get_db)):
    return db.query(User).filter(User.role == "provider").all()

