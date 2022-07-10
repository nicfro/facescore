import os
import sys
sys.path.insert(0, os.getcwd())

import sqlalchemy
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from src.orm_models.db_models import UserModel
from . import DBC
from src.logic.hasher import Hasher
from src.logic.jwt_handler import JWT_Handler


hasher = Hasher()
router = APIRouter()
JWT = JWT_Handler()


@router.get("/login")
def login_user(user_name: str, password: str, db: Session = Depends(DBC.get_session)):
    """
    GET login token for user
    :param user_name: User ID to log in
    :param db: DB session
    :return: Retrieved login token
    """
    try:
        user = db.query(UserModel).filter(UserModel.name == user_name).one()
        if hasher.verify(password, user.salt, str(user.hashed_password)):
            token = JWT.encode_auth_token(user.id, 10000)
            return {"jwt_token": token}
        else:
            return {"jwt_token": "wrong password"}

    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"{user_name} does not exist")