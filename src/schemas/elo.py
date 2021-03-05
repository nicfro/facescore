from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class EloSchema(BaseModel):
    """
    Elo database table schema
    It holds all column names and relationship to other tables
    """
    id: int
    image_id: int
    score: int
    created_at: datetime.datetime
    class Config:
        orm_mode = True


class EloCreate(BaseModel):
    """
    Fields information needed for POST
    """
    image_id: int
    score: int


class UserUpdate(BaseModel):
    """
    Fields information needed for Update
    """
    id: int
    image_id: int
    score: int



class UserDelete(BaseModel):
    """
    Fields information needed for Delete
    """
    id: int
