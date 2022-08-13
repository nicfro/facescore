from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from datetime import date


class UserSchema(BaseModel):
    """
    AnnotationTypes database table schema
    It holds all column names and relationship to other tables
    """

    id: int
    name: str
    email: str
    gender: Optional[str]
    country: Optional[str]
    hashed_password: str
    birthdate: Optional[date]
    salt: str
    points: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    """
    Fields information needed for POST
    """

    name: str
    email: str
    password: str


class UserUpdate(BaseModel):
    """
    Fields information needed for Update
    """

    gender: Optional[str]
    email: Optional[str]
    country: Optional[str]
    birthdate: Optional[date]
