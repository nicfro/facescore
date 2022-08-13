import os
import sys

sys.path.insert(0, os.getcwd())


from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from src.schemas.users import UserSchema
from src.schemas.token import TokenData
from fastapi.security import OAuth2PasswordBearer
from src.orm_models.db_models import UserModel
from src.database.base import DBConnector
from src.logic.jwt_handler import JWT_Handler

DBC = DBConnector()
JWT_test = JWT_Handler()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(DBC.get_session)
):
    """
    fetches current user using oauth2 validation
    Query with header where
    key is: Authorization
    value is: bearer JWT_token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        user_id = JWT_test.decode_auth_token(token)["sub"]
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except:
        raise credentials_exception

    user = db.query(UserModel).filter(UserModel.id == token_data.user_id).one_or_none()
    if user is None:
        raise credentials_exception

    return UserSchema(
        id=user.id,
        name=user.name,
        email=user.email,
        gender=user.gender,
        country=user.country,
        hashed_password=str(user.hashed_password),
        birthdate=user.birthdate,
        salt=user.salt,
        points=user.points,
        created_at=user.created_at,
    )
