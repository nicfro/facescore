from typing import List
import sqlalchemy
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from ..schemas.votes import VoteSchema, VoteCreate, VoteDelete, VoteUpdate
from ..orm_models.db_models import VoteModel
from . import DBC
from src.logic.hasher import Hasher


hasher = Hasher()
router = APIRouter()


@router.get("/votes", response_model=List[VoteSchema])
def get_all_votes(db: Session = Depends(DBC.get_session)):
    """
    GET all votes
    :param db: DB session
    :return: ALl vote entries
    """
    return [{"id": vote.id,
             "user_id": vote.user_id,
             "left_image_id": vote.left_image_id, 
             "right_image_id": vote.right_image_id} for vote in db.query(VoteModel).all()]


@router.get("/votes/user/{user_id}", response_model=VoteSchema)
def get_one_vote_by_user_id(user_id: str, db: Session = Depends(DBC.get_session)):
    """
    GET one vote by name
    :param vote_name: Vote name to get
    :param db: DB session
    :return: Retrieved vote entry
    """
    try:
        # Get vote by name
        vote = db.query(VoteModel).filter(VoteModel.user_id == user_id).all()
        return {"id": vote.id,
                "user_id": vote.user_id,
                "left_image_id": vote.left_image_id, 
                "right_image_id": vote.right_image_id}
    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"User {user_id} does not exist")


@router.get("/votes/id/{vote_id}", response_model=VoteSchema)
def get_one_vote_by_id(vote_id: str, db: Session = Depends(DBC.get_session)):
    """
    GET one vote by ID
    :param vote_id: Vote ID to get
    :param db: DB session
    :return: Retrieved vote entry
    """
    try:
        # Get vote by name
        vote = db.query(VoteModel).filter(VoteModel.id == vote_id).one()
        return {"id": vote.id,
                "user_id": vote.user_id,
                "left_image_id": vote.left_image_id, 
                "right_image_id": vote.right_image_id}
    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"{vote_id} does not exist")


@router.post("/votes", response_model=VoteSchema)
def post_one_vote(vote: VoteCreate, db: Session = Depends(DBC.get_session)):
    """
    POST one vote
    It reads parameters from the request field and add missing fields from default values defined in the model
    :param vote: VoteBase class that contains all columns in the table
    :param db: DB session
    :return: Created vote entry
    """
    vote_to_create = VoteModel(**vote.dict())

    # Commit to DB
    db.add(vote_to_create)
    db.commit()
    db.refresh(vote_to_create)


@router.delete("/votes/id/{vote_id}", response_model=VoteDelete)
def delete_one_vote_by_id(vote_id: str, db: Session = Depends(DBC.get_session)):
    """
    DELETE one vote by ID
    It reads parameters from the request field, finds the entry and delete it
    :param vote_id: Vote ID to delete
    :param db: DB session
    :return: Deleted vote entry
    """
    try:
        # Delete entry
        affected_rows = db.query(VoteModel).filter(VoteModel.id == vote_id).delete()
        if not affected_rows:
            raise sqlalchemy.orm.exc.NoResultFound
        # Commit to DB
        db.commit()
        return {"id": vote.id}
    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"{vote_id} does not exist")
