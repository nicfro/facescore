from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List, Literal
from datetime import datetime, date
import re


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
    embedding1: Optional[List]
    embedding2: Optional[List]
    verified: Optional[bool]

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    """
    Fields information needed for POST
    """

    name: str
    email: EmailStr
    password1: str
    password2: str

    @validator("password2")
    def passwords_match_and_legal(cls, v, values, **kwargs):
        if v != values["password1"]:
            raise ValueError("passwords do not match")
        if len(v) < 8:
            raise ValueError("Make sure your password is at lest 8 letters")
        elif re.search("[0-9]", v) is None:
            raise ValueError("Make sure your password has a number in it")
        elif re.search("[A-Z]", v) is None:
            raise ValueError("Make sure your password has a capital letter in it")
        else:
            return v


class UserUpdate(BaseModel):
    """
    Fields information needed for Update
    """

    gender: Optional[str]
    country: Optional[str]
    birthdate: Optional[date]


class UserVerificationRequest(BaseModel):
    """
    Fields for verification request
    """

    image: str
    gesture: Literal[
        "peace", "call", "dislike", "ok", "like", "one", "stop inverted", "palm", "rock"
    ]


class UserVerificationResponse(BaseModel):
    """
    Fields for verification response
    """

    verified: bool
    missing_embeddings: int
