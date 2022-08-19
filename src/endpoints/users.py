import os
import sys
import requests
import json

sys.path.insert(0, os.getcwd())

import sqlalchemy
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, UploadFile, File
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
from src.logic.auth import get_current_user
from src.utils.custom_error_handlers import forbidden_exception


hasher = Hasher()
router = APIRouter()
jwt = JWT_Handler()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

ACCESS_TOKEN_EXPIRE_SECONDS = int(os.environ.get("ACCESS_TOKEN_EXPIRE_SECONDS"))
POINTS_USER_META_DATA_AWARD = int(os.environ.get("POINTS_USER_META_DATA_AWARD"))
ML_ENDPOINT = os.environ.get("ML_ENDPOINT")


@router.get("/users/me/", response_model=UserSchema)
async def get_me(current_user: UserSchema = Depends(get_current_user)):
    """
    GET current user from token
    :param token: User token
    :param db: DB session
    :return: Retrieved user entry
    """
    return current_user


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
        db.refresh(user)

        return {"access_token": token, "token_type": "bearer"}

    except sqlalchemy.exc.IntegrityError:
        raise Exception(f"Duplicate Email: {user.email} or Username: {user.name}")


@router.post("/users/verify/", response_model=UserVerificationResponse)
async def verify_user(
    user_verification: UserVerificationRequest,
    current_user: UserSchema = Depends(get_current_user),
    db: Session = Depends(DBC.get_session),
):

    headers = {"Content-type": "application/json", "Accept": "text/plain"}
    payload = json.dumps({"image": user_verification.image, "gesture": "ok"})

    response = requests.post(ML_ENDPOINT, data=payload, headers=headers)
    data = response.json()
    if current_user.embedding1 is None:
        current_user.embedding1 = data["embedding"]
        db.commit()
        return UserVerificationResponse(verified=False, missing_embeddings=1)

    if current_user.embedding2 is None:
        current_user.embedding2 = data["embedding"]
        db.commit()
        return UserVerificationResponse(verified=True, missing_embeddings=0)

    return forbidden_exception("User is already verified")


@router.put("/users", response_model=UserSchema)
def put_one_user(
    user: UserUpdate,
    current_user: UserSchema = Depends(get_current_user),
    db: Session = Depends(DBC.get_session),
):
    """
    PUT one user
    It reads parameters from the request field and update finds the entry and update it
    :param user: UserUpdate class that contains requested field to update
    :param db: DB session
    :return: Updated user entry
    """
    try:
        # Get user by ID
        user_to_put = db.query(UserModel).filter(UserModel.id == current_user.id).one()

        # Update model class variable for requested fields
        for var, value in vars(user).items():
            if value:
                if getattr(user_to_put, var) is None:
                    user_to_put.points += POINTS_USER_META_DATA_AWARD
                setattr(user_to_put, var, value)
            else:
                getattr(user_to_put, var)

        # Commit to DB
        db.add(user_to_put)
        db.commit()
        db.refresh(user_to_put)
        return {
            "id": user_to_put.id,
            "name": user_to_put.name,
            "email": user_to_put.email,
            "gender": user_to_put.gender,
            "country": user_to_put.country,
            "hashed_password": str(user_to_put.hashed_password),
            "birthdate": user_to_put.birthdate,
            "salt": user_to_put.salt,
            "points": user_to_put.points,
            "created_at": user_to_put.created_at,
        }

    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"{user.id} does not exist")


@router.delete("/users/", response_model=UserSchema)
def delete_current_user(
    current_user: UserSchema = Depends(get_current_user),
    db: Session = Depends(DBC.get_session),
):
    """
    Deletes current user
    :return: Deleted user entry
    """
    try:
        # Delete entry
        affected_rows = (
            db.query(UserModel).filter(UserModel.id == current_user.id).delete()
        )
        if not affected_rows:
            raise sqlalchemy.orm.exc.NoResultFound
        # Commit to DB
        db.commit()
        return current_user
    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"{current_user.id} does not exist")
