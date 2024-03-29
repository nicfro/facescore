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
    file: str
    created_at: datetime

    class Config:
        orm_mode = True


class ImageCreateRequest(BaseModel):
    """
    Fields information needed for POST
    """

    image: str


class ImageCreateResponse(BaseModel):
    """
    Fields information needed for POST
    """

    image_id: int
    elo_mu: float
    elo_sigma: float


class ImageUpdate(BaseModel):
    """
    Fields information needed for Update
    """

    id: int
    user_id: Optional[int]
    file: str
