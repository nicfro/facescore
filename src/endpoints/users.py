import os
import sys
import requests
import json
from typing import Tuple

sys.path.insert(0, os.getcwd())

import sqlalchemy
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from src.schemas.users import (
    UserSchema,
    UserCreate,
    UserUpdate,
    UserVerificationRequest,
    UserVerificationResponse,
)
from src.schemas.token import TokenSchema
from fastapi.security import OAuth2PasswordBearer
from src.orm_models.db_models import UserModel
from . import DBC
from src.logic.hasher import Hasher
from src.logic.jwt_handler import JWT_Handler
from src.logic.auth import get_current_user_db
from src.utils.custom_error_handlers import forbidden_exception


hasher = Hasher()
router = APIRouter()
jwt = JWT_Handler()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

ACCESS_TOKEN_EXPIRE_SECONDS = int(os.environ.get("ACCESS_TOKEN_EXPIRE_SECONDS"))
POINTS_USER_META_DATA_AWARD = int(os.environ.get("POINTS_USER_META_DATA_AWARD"))
ML_ENDPOINT = os.environ.get("ML_ENDPOINT")


@router.get("/users/me/", response_model=UserSchema)
async def get_me(
    current_user: Tuple[UserSchema, Session] = Depends(get_current_user_db)
):
    """
    GET current user from token
    :param token: User token
    :param db: DB session
    :return: Retrieved user entry
    """
    return current_user[0]


@router.post("/users", response_model=TokenSchema)
async def post_one_user(user: UserCreate, db: Session = Depends(DBC.get_session)):
    """
    POST one user
    It reads parameters from the request field and add missing fields from default values defined in the model
    :param user: UserBase class that contains all columns in the table
    :param db: DB session
    :return: TokenSchema
    """

    user_args = user.dict()
    # Create hashed password
    user_args["hashed_password"], user_args["salt"] = hasher.user_hash(user.password1)

    # Create User Model
    del user_args["password1"]
    del user_args["password2"]
    user_args["name"] = user_args["name"].lower()
    user = UserModel(**user_args)
    try:
        db.add(user)
        # flush for fetching id
        db.flush()
        token = jwt.encode_auth_token(user.id, ACCESS_TOKEN_EXPIRE_SECONDS)
        db.commit()
        return {"access_token": token, "token_type": "bearer"}

    except sqlalchemy.exc.IntegrityError:
        raise Exception(f"Duplicate Email: {user.email} or Username: {user.name}")


@router.post("/users/verify/", response_model=UserVerificationResponse)
def verify_user(
    user_verification: UserVerificationRequest,
    current_user_db: Tuple[UserSchema, Session] = Depends(get_current_user_db),
):
    current_user, db = current_user_db

    headers = {"Content-type": "application/json", "Accept": "text/plain"}
    payload = json.dumps(
        {"image": user_verification.image, "gesture": user_verification.gesture}
    )
    response = requests.post(
        ML_ENDPOINT + "detections/gestures", data=payload, headers=headers
    )

    if response.status_code == 200:
        data = response.json()
        if current_user.embedding1 is None:
            current_user.embedding1 = data["embedding"]
            db.commit()
            return UserVerificationResponse(verified=False, missing_embeddings=1)
        elif current_user.embedding2 is None:
            current_user.embedding2 = data["embedding"]
            current_user.verified = True
            db.commit()
            return UserVerificationResponse(verified=True, missing_embeddings=0)
        else:
            raise forbidden_exception("User is already verified")

    else:
        raise forbidden_exception(response.json()["detail"])


@router.put("/users", response_model=UserSchema)
def put_one_user(
    user_update: UserUpdate,
    current_user_db: Tuple[UserSchema, Session] = Depends(get_current_user_db),
):
    """
    PUT one user
    It reads parameters from the request field and update finds the entry and update it
    :param user: UserUpdate class that contains requested field to update
    :param db: DB session
    :return: Updated user entry
    """
    current_user, db = current_user_db

    # Update model class variable for requested fields
    for var, value in vars(user_update).items():
        if value:
            if getattr(current_user, var) is None:
                current_user.points += POINTS_USER_META_DATA_AWARD
            setattr(current_user, var, value)
        else:
            getattr(current_user, var)

    db.commit()
    return current_user


@router.delete("/users/", response_model=UserSchema)
def delete_current_user(
    current_user_db: Tuple[UserSchema, Session] = Depends(get_current_user_db),
):
    """
    Deletes current user
    :return: Deleted user entry
    """
    current_user, db = current_user_db
    db.delete(current_user)
    db.commit()
    return current_user
