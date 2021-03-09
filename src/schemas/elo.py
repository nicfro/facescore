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
    mu: float
    sigma: float
    created_at: datetime
    class Config:
        orm_mode = True


class EloCreate(BaseModel):
    """
    Fields information needed for POST
    """
    image_id: int


class EloUpdate(BaseModel):
    """
    Fields information needed for Update
    """
    id: int
    image_id: Optional[int]
    mu: Optional[float]
    sigma: Optional[float]



class EloDelete(BaseModel):
    """
    Fields information needed for Delete
    """
    id: int
