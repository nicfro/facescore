from typing import List
import sqlalchemy
from sqlalchemy import select, func, table, tablesample
from sqlalchemy.orm import Session, aliased, load_only
from fastapi import Depends, APIRouter, UploadFile, File, Form
from ..schemas.images import ImageSchema
from ..orm_models.db_models import ImageModel
from . import DBC, S3
from ..orm_models.db_models import EloModel
from src.logic.hasher import Hasher

import base64


hasher = Hasher()
router = APIRouter()

@router.post("/images")
async def post_image(gender: str = Form(...), user_id: int = Form(...), image: UploadFile = File(...), db: Session = Depends(DBC.get_session)):
    
    """
    POST one image to database if sucessful also to S3
    Gets user_id & Gender from form and file as an UploadFile object
    :param user_id: the user id of the image
    :param file: the file to be uploaded
    :param db: DB session
    :return: Created image entry
    """

    # Store image in S3
    image_file = image.file.read()
    image_file = base64.b64encode(image_file)

    image_name = f"images/{gender}/{hasher.image_hash(image_file)}"

    image_args = {"user_id": user_id,
                  "file": image_name}
    image_model = ImageModel(**image_args)
    db.add(image_model)
    db.commit()

    elo_args = {"image_id": image_model.id}
    elo_model = EloModel(**elo_args)
    
    S3_response = S3.upload_image(image_file, image_name)

    db.add(elo_model)
    db.commit()
    
    if S3_response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return {"message": f"Image created with id: {image_model.id} with eloscore {elo_model.mu, elo_model.sigma}"}

    db.rollback()
    return {"message": f"Error uploading to S3 {S3_response}"}


@router.get("/images/votes", response_model=List[ImageSchema])
async def get_image_for_vote(db: Session = Depends(DBC.get_session)):
    """
    GET two images that are relatively close in score
    :param image_id: identifier for the image to be returned
    :param db: DB session
    :return: image paths and users
    """

    return [{"id": image.id,
             "user_id": image.user_id,
             "file": image.file,
             "created_at": image.created_at} for image in db.query(ImageModel).order_by(func.random()).limit(2).all()]


@router.get("/images/id/{image_id}", response_model=ImageSchema)
async def get_image_by_id(image_id: int, db: Session = Depends(DBC.get_session)):
    """
    GET one image 
    Get image_id from form
    :param image_id: identifier for the image to be returned
    :param db: DB session
    :return: image as binary data
    """
    try:
        # Get user by name
        image = db.query(ImageModel).filter(ImageModel.id == image_id).one()
        return {"id": image.id,
                "user_id": image.user_id,
                "file": image.file, 
                "created_at": image.created_at}
    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"{image_id} does not exist")


