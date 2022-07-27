import os
import sys

sys.path.insert(0, os.getcwd())

from typing import List
import sqlalchemy
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from src.schemas.votes import VoteSchema, VoteCreate, VoteDelete
from src.orm_models.db_models import VoteModel
from . import DBC
from src.logic.elo import calculateElo
from src.orm_models.db_models import EloModel

router = APIRouter()


@router.post("/votes")
def post_one_vote(vote: VoteCreate, db: Session = Depends(DBC.get_session)):
    """
    POST one vote
    It reads parameters from the request field and add missing fields from default values defined in the model
    :param vote: VoteBase class that contains all columns in the table
    :param db: DB session
    :return: Created vote entry
    """
    try:
        vote_to_create = VoteModel(**vote.dict())

        winner = vote_to_create.winner_image_id
        loser = vote_to_create.loser_image_id

        scores = calculateElo(winner, loser)

        elo_args_winner = {
            "image_id": winner,
            "mu": scores["winner_mu"],
            "sigma": scores["winner_sigma"],
        }

        elo_model_winner = EloModel(**elo_args_winner)

        elo_args_loser = {
            "image_id": loser,
            "mu": scores["loser_mu"],
            "sigma": scores["loser_sigma"],
        }

        elo_model_loser = EloModel(**elo_args_loser)

        objects = [elo_model_winner, elo_model_loser, vote_to_create]
        db.bulk_save_objects(objects)

        db.commit()
        return {"message": f"Vote was cast on image: {winner} and {loser}"}
    except sqlalchemy.exc.IntegrityError:
        raise Exception(f"User or images does not exist")
