from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ImageSchema(BaseModel):
    """
    Images database table schema
    It holds all column names and relationship to other tables
    """
    id: int
    user_id: int
    created_at: datetime.datetime
    file: bytearray

    class Config:
        orm_mode = True

class ImageCreate(BaseModel):
    """
    Fields information needed for POST
    """
    user_id: int
    created_at: Optional[datetime.datetime]
    file: bytearray 


class ImageUpdate(BaseModel):
    """
    Fields information needed for Update
    """
    id: int
    user_id: int
    file: bytearray


class UserDelete(BaseModel):
    """
    Fields information needed for Delete
    """
    id: int
