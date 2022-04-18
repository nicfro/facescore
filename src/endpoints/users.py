from msilib.schema import Error
from typing import List
import sqlalchemy
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from ..schemas.users import UserSchema, UserCreate, UserDelete, UserUpdate
from ..orm_models.db_models import UserModel
from . import DBC
from src.logic.hasher import Hasher


hasher = Hasher()
router = APIRouter()


@router.get("/users", response_model=List[UserSchema])
def get_all_users(db: Session = Depends(DBC.get_session)):
    """
    GET all users
    :param db: DB session
    :return: ALl user entries
    """
    return [{"id": user.id,
             "name": user.name,
             "email": user.email, 
             "gender": user.gender,
             "country": user.country,
             "hashed_password": str(user.hashed_password), 
             "birthdate": user.birthdate,
             "salt": user.salt,
             "created_at": user.created_at} for user in db.query(UserModel).all()]


@router.get("/users/name/{user_name}", response_model=UserSchema)
def get_one_user_by_name(user_name: str, db: Session = Depends(DBC.get_session)):
    """
    GET one user by name
    :param user_name: User name to get
    :param db: DB session
    :return: Retrieved user entry
    """
    try:
        # Get user by name
        user = db.query(UserModel).filter(UserModel.name == user_name).one()
        return {"id": user.id,
                "name": user.name,
                "email": user.email, 
                "gender": user.gender,
                "country": user.country,
                "hashed_password": str(user.hashed_password), 
                "birthdate": user.birthdate,
                "salt": user.salt,
                "created_at": user.created_at}
    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"{user_name} does not exist")


@router.get("/users/id/{user_id}", response_model=UserSchema)
def get_one_user_by_id(user_id: str, db: Session = Depends(DBC.get_session)):
    """
    GET one user by ID
    :param user_id: User ID to get
    :param db: DB session
    :return: Retrieved user entry
    """
    try:
        # Get user by name
        user = db.query(UserModel).filter(UserModel.id == user_id).one()
        return {"id": user.id,
                "name": user.name,
                "email": user.email, 
                "gender": user.gender,
                "country": user.country,
                "hashed_password": str(user.hashed_password), 
                "birthdate": user.birthdate,
                "salt": user.salt,
                "created_at": user.created_at}
    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"{user_id} does not exist")



@router.post("/users", response_model=UserSchema)
def post_one_user(user: UserCreate, db: Session = Depends(DBC.get_session)):
    """
    POST one user
    It reads parameters from the request field and add missing fields from default values defined in the model
    :param user: UserBase class that contains all columns in the table
    :param db: DB session
    :return: Created user entry
    """
    try:
        user_args = user.dict()
        # Create hashed passwordxw
        user_args["hashed_password"], user_args["salt"] = hasher.user_hash(user.password)    

        # Create User Model
        del user_args['password']
        user_args["name"] = user_args["name"].lower()
        user = UserModel(**user_args)

        # Commit to DB
        db.add(user)
        db.commit()
        db.refresh(user)
        return {"id": user.id,
                "name": user.name,
                "email": user.email, 
                "gender": user.gender,
                "country": user.country,
                "hashed_password": str(user.hashed_password), 
                "birthdate": user.birthdate,
                "salt": user.salt,
                "created_at": user.created_at}

    except sqlalchemy.exc.IntegrityError:
        raise Exception(f"Duplicate Email: {user.email} or Username: {user.name}")


@router.put("/users", response_model=UserSchema)
def put_one_user(user: UserUpdate, db: Session = Depends(DBC.get_session)):
    """
    PUT one user
    It reads parameters from the request field and update finds the entry and update it
    :param user: UserUpdate class that contains requested field to update
    :param db: DB session
    :return: Updated user entry
    """
    try:
        # Get user by ID
        user_to_put = db.query(UserModel).filter(UserModel.id == user.id).one()

        # Update model class variable for requested fields
        for var, value in vars(user).items():
            setattr(user_to_put, var, value) if value else getattr(user_to_put,var)

        # Commit to DB
        db.add(user_to_put)
        db.commit()
        db.refresh(user_to_put)
        return {"id": user_to_put.id,
                "name": user_to_put.name,
                "email": user_to_put.email, 
                "gender": user_to_put.gender,
                "country": user_to_put.country,
                "hashed_password": str(user_to_put.hashed_password), 
                "birthdate": user_to_put.birthdate,
                "salt": user_to_put.salt,
                "created_at": user_to_put.created_at}

    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"{user.id} does not exist")


@router.delete("/users/id/{user_id}", response_model=UserDelete)
def delete_one_user_by_id(user_id: str, db: Session = Depends(DBC.get_session)):
    """
    DELETE one user by ID
    It reads parameters from the request field, finds the entry and delete it
    :param user_id: User ID to delete
    :param db: DB session
    :return: Deleted user entry
    """
    try:
        # Delete entry
        affected_rows = db.query(UserModel).filter(UserModel.id == user_id).delete()
        if not affected_rows:
            raise sqlalchemy.orm.exc.NoResultFound
        # Commit to DB
        db.commit()
        return {"id": user_id}
    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"{user_id} does not exist")
