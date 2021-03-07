from typing import List
import sqlalchemy
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from ..schemas.images import ImageSchema, ImageCreate
from ..orm_models.db_models import ImageModel
from . import DBC
from src.logic.hasher import Hasher


router = APIRouter()



@router.post("/images", response_model=ImageSchema)
def post_one_user(image: ImageCreate, db: Session = Depends(DBC.get_session)):
    """
    POST one image
    It reads parameters from the request field and add missing fields from default values defined in the model
    :param user: UserBase class that contains all columns in the table
    :param db: DB session
    :return: Created user entry
    """
    image_args = image.dict()
    image_model = ImageModel(**image_args)

    # Commit to DB
    db.add(image_model)
    db.commit()
    db.refresh(image_model)
    return {"message": f"user with created with id: {image_model.id}"}
