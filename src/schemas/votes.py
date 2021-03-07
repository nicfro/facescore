from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class VoteSchema(BaseModel):
    """
    Images database table schema
    It holds all column names and relationship to other tables
    """
    id: int
    user_id: int
    left_image_id: int
    right_image_id: int
    winner: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True

class VoteCreate(BaseModel):
    """
    Fields information needed for POST
    """
    user_id: int
    left_image_id: int
    right_image_id: int
    winner: int

class VoteUpdate(BaseModel):
    """
    Fields information needed for Update
    """
    id: int
    user_id: Optional[int]
    left_image_id: Optional[int]
    right_image_id: Optional[int]
    winner: Optional[int]


class VoteDelete(BaseModel):
    """
    Fields information needed for Delete
    """
    id: int
