# crud.py
from sqlalchemy.orm import Session
from .models import User
from .schemas import UserCreate

def get_user_by_nfc_id(db: Session, nfc_id: str):
    return db.query(User).filter(User.nfc_id == nfc_id).first()

def create_user(db: Session, user: UserCreate):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user