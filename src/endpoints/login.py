import os
import sys


sys.path.insert(0, os.getcwd())

from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from src.orm_models.db_models import UserModel
from src.schemas.token import TokenSchema
from . import DBC
from src.logic.hasher import Hasher
from src.logic.jwt_handler import JWT_Handler


hasher = Hasher()
router = APIRouter()
jwt = JWT_Handler()
ACCESS_TOKEN_EXPIRE_SECONDS = int(os.environ.get("ACCESS_TOKEN_EXPIRE_SECONDS"))


@router.get("/login", response_model=TokenSchema)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(DBC.get_session),
):
    """
    GET login token for user
    :param user_name: User ID to log in
    :param db: DB session
    :return: Retrieved login token
    """
    login_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = (
        db.query(UserModel)
        .filter(UserModel.name == form_data.username.lower())
        .one_or_none()
    )
    if user:
        if hasher.verify(form_data.password, user.salt, str(user.hashed_password)):
            token = jwt.encode_auth_token(user.id, ACCESS_TOKEN_EXPIRE_SECONDS)
            return {"access_token": token, "token_type": "bearer"}
        else:
            raise login_exception
    else:
        raise login_exception
