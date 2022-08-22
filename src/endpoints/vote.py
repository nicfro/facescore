import os
import sys
from typing import Tuple

sys.path.insert(0, os.getcwd())

from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException, status
from src.settings import load_config
from src.schemas.votes import VoteCreate
from src.schemas.users import UserSchema
from src.orm_models.db_models import VoteModel, EloModel
from src.logic.elo import calculateElo
from . import DBC
from src.logic.auth import get_current_user_db

router = APIRouter()

if os.path.isfile("ENV"):
    load_config("ENV")

POINTS_VOTE_AWARD = os.environ.get("POINTS_VOTE_AWARD")


@router.post("/votes", response_model=VoteCreate)
def post_one_vote(
    vote: VoteCreate,
    current_user_db: Tuple[UserSchema, Session] = Depends(get_current_user_db),
):
    """
    POST one vote
    Gets user_id from current user, receives winner/loser ID from post
    :param vote: VoteBase class that contains winner/loser image ID
    :return: Created vote entry
    """
    current_user, db = current_user_db
    try:
        payload = {
            "user_id": current_user.id,
            "loser_image_id": vote.dict()["loser_image_id"],
            "winner_image_id": vote.dict()["winner_image_id"],
        }

        vote_to_create = VoteModel(**payload)

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

        current_user.points += int(POINTS_VOTE_AWARD)

        objects = [elo_model_winner, elo_model_loser, vote_to_create, current_user]
        db.bulk_save_objects(objects)

        db.commit()

        return {
            "user_id": vote_to_create.user_id,
            "loser_image_id": vote_to_create.loser_image_id,
            "winner_image_id": vote_to_create.winner_image_id,
        }
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User or images does not exist",
            headers={"WWW-Authenticate": "Bearer"},
        )
