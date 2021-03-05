from typing import List
import sqlalchemy
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from ..schemas.users import UserSchema
from ..orm_models.db_models import UserModel
from . import DBC
from src.logic.hasher import Hasher
from src.logic.jwt_handler import encode_auth_token


hasher = Hasher()
router = APIRouter()


@router.get("/login/{user_id}")
def login_user_by_id(user_id: str, user_password: str, db: Session = Depends(DBC.get_session)):
    """
    GET login token for user
    :param user_id: User ID to log in
    :param db: DB session
    :return: Retrieved login token
    """
    try:
        user = db.query(UserModel).filter(UserModel.id == user_id).one()
        if hasher.verify(user_password, user.salt, str(user.hashed_password)):
            return {"jwt_token": encode_auth_token(user.id, 1000)}
        else:
            return {"jwt_token": None}

    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"{user_id} does not exist")