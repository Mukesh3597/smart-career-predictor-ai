from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    full_name: str
    email: Optional[EmailStr] = None

class UserOut(BaseModel):
    id: int
    full_name: str
    email: Optional[EmailStr] = None

    class Config:
        from_attributes = True