from typing import List
import sqlalchemy
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from ..schemas.elos import EloSchema, EloCreate, EloDelete, EloUpdate
from ..orm_models.db_models import EloModel
from . import DBC

router = APIRouter()


@router.get("/elos", response_model=List[EloSchema])
def get_all_elos(db: Session = Depends(DBC.get_session)):
    """
    GET all elos
    :param db: DB session
    :return: ALl elo entries
    """
    return [{"id": elo.id,
             "image_id": elo.image_id,
             "score": elo.score
             "created_at": elo.created_at}]


@router.get("/elos/image/{image_id}", response_model=EloSchema)
def get_one_elo_by_image_id(image_id: str, db: Session = Depends(DBC.get_session)):
    """
    GET one elo by image_id
    :param elo_name: Elo name to get
    :param db: DB session
    :return: Retrieved elo entry
    """
    try:
        # Get elo by name
        elo = db.query(EloModel).filter(EloModel.image_id == image_id).all()
        return {"id": elo.id,
                "image_id": elo.image_id,
                "score": elo.score
                "created_at": elo.created_at}
    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"User {elo_id} does not exist")


@router.get("/elos/id/{elo_id}", response_model=EloSchema)
def get_one_elo_by_id(elo_id: str, db: Session = Depends(DBC.get_session)):
    """
    GET one elo by ID
    :param elo_id: Elo ID to get
    :param db: DB session
    :return: Retrieved elo entry
    """
    try:
        # Get elo by name
        elo = db.query(EloModel).filter(EloModel.id == elo_id).one()
        return {"id": elo.id,
                "image_id": elo.image_id,
                "score": elo.score
                "created_at": elo.created_at}
    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"{elo_id} does not exist")


@router.post("/elos", response_model=EloSchema)
def post_one_elo(elo: EloCreate, db: Session = Depends(DBC.get_session)):
    """
    POST one elo
    It reads parameters from the request field and add missing fields from default values defined in the model
    :param elo: EloBase class that contains all columns in the table
    :param db: DB session
    :return: Created elo entry
    """
    elo_to_create = EloModel(**elo.dict())

    # Commit to DB
    db.add(elo_to_create)
    db.commit()
    db.refresh(elo_to_create)


@router.delete("/elos/id/{elo_id}", response_model=EloDelete)
def delete_one_elo_by_id(elo_id: str, db: Session = Depends(DBC.get_session)):
    """
    DELETE one elo by ID
    It reads parameters from the request field, finds the entry and delete it
    :param elo_id: Elo ID to delete
    :param db: DB session
    :return: Deleted elo entry
    """
    try:
        # Delete entry
        affected_rows = db.query(EloModel).filter(EloModel.id == elo_id).delete()
        if not affected_rows:
            raise sqlalchemy.orm.exc.NoResultFound
        # Commit to DB
        db.commit()
        return {"id": elo.id}
    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"{elo_id} does not exist")
