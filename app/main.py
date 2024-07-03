# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .app import crud
from . import models, schemas, database

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.database.disconnect()

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.UserDisplay)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_nfc_id(db, nfc_id=user.nfc_id)
    if db_user:
        raise HTTPException(status_code=400, detail="NFC ID already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/{nfc_id}", response_model=schemas.UserDisplay)
async def read_user(nfc_id: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_nfc_id(db, nfc_id=nfc_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
