# schemas.py
from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    email: str
    nfc_id: str

class UserCreate(UserBase):
    pass

class UserDisplay(UserBase):
    id: int

    class Config:
        orm_mode = True
