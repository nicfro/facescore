from pydantic import BaseModel
from typing import Optional
from datetime import date


class UserSchema(BaseModel):
    """
    AnnotationTypes database table schema
    It holds all column names and relationship to other tables
    """
    id: int
    name: str
    email: str
    gender: str
    country: str
    hashed_password: str
    birthdate: date
    salt: str

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    """
    Fields information needed for POST
    """
    name: str
    email: str
    gender: str
    country: str
    password: str
    birthdate: Optional[date]

class UserUpdate(BaseModel):
    """
    Fields information needed for Update
    """
    id: int
    name: Optional[str]
    email: Optional[str]
    gender: Optional[str]
    country: Optional[str]
    birthdate: Optional[date]
    salt: str


class UserDelete(BaseModel):
    """
    Fields information needed for Delete
    """
    id: int
