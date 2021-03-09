from typing import List
import sqlalchemy
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from ..schemas.elo import EloSchema, EloCreate
from ..orm_models.db_models import EloModel
from . import DBC
from src.logic.hasher import Hasher

router = APIRouter()


@router.get("/elo/image_id/{image_id}", response_model=EloSchema)
def get_elo_by_image_id(image_id: int, db: Session = Depends(DBC.get_session)):
    """
    GET elo score by image_id
    :param image_id: image_id you want the elo score of
    :param db: DB session
    :return: Elo score for image with image_id
    """
    try:
        # Get user by name
        elo = db.query(EloModel).filter(EloModel.image_id == image_id).order_by(EloModel.id.desc()).first()
        return {"id": elo.id,
                "image_id": elo.image_id,
                "mu": elo.mu, 
                "sigma": elo.sigma, 
                "created_at": elo.created_at}
    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"Elo score for image with image_id: {image_id} does not exist")



@router.post("/elo")
def post_elo_score(elo: EloCreate, db: Session = Depends(DBC.get_session)):
    """
    POST elo score
    It reads parameters from the request field and add missing fields from default values defined in the model
    :param elo: EloBase class that contains all columns in the table
    :param db: DB session
    :return: Created user entry
    """
    elo_args = elo.dict()
    elo_model = EloModel(**elo_args)

    # Commit to DB
    db.add(elo_model)
    db.commit()
    db.refresh(elo_model)
    return {"message": f"Elo score created with id: {elo_model.id}"}
