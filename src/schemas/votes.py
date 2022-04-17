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
    loser_image_id: Optional[int]
    winner_image_id: Optional[int]
    created_at: datetime

    class Config:
        orm_mode = True

class VoteCreate(BaseModel):
    """
    Fields information needed for POST
    """
    user_id: int
    loser_image_id: Optional[int]
    winner_image_id: Optional[int]

class VoteUpdate(BaseModel):
    """
    Fields information needed for Update
    """
    id: int
    user_id: Optional[int]
    loser_image_id: Optional[int]
    winner_image_id: Optional[int]


class VoteDelete(BaseModel):
    """
    Fields information needed for Delete
    """
    id: int
