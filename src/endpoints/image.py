import os
import sys
import base64
from typing import List

sys.path.insert(0, os.getcwd())

import sqlalchemy
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, UploadFile, File, HTTPException, status
from src.schemas.images import ImageSchema
from src.schemas.users import UserSchema
from src.orm_models.db_models import ImageModel, EloModel, UserModel
from . import DBC, S3
from src.logic.hasher import Hasher
from src.logic.auth import get_current_user
from src.settings import load_config

hasher = Hasher()
router = APIRouter()

if os.path.isfile("ENV"):
    load_config("ENV")

POINTS_UPLOAD_COST = os.environ.get("POINTS_UPLOAD_COST")


@router.post("/images")
async def post_image(
    current_user: UserSchema = Depends(get_current_user),
    image: UploadFile = File(...),
    db: Session = Depends(DBC.get_session),
):

    """
    POST one image to database if sucessful also to S3
    Gets user_id & Gender from form and file as an UploadFile object
    :param user_id: the user id of the image
    :param file: the file to be uploaded
    :param db: DB session
    :return: Created image entry
    """

    if current_user.points < 10:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not enough points for image upload",
        )

    # Store image in S3
    image_file = image.file.read()
    image_file = base64.b64encode(image_file)

    image_name = f"images/{current_user.gender}/{hasher.image_hash(image_file)}"

    image_args = {"user_id": current_user.id, "file": image_name}
    image_model = ImageModel(**image_args)
    db.add(image_model)
    db.commit()

    elo_args = {"image_id": image_model.id}
    elo_model = EloModel(**elo_args)

    db.add(elo_model)
    db.commit()

    S3_response = S3.upload_image(image_file, image_name)

    user_to_put = db.query(UserModel).filter(UserModel.id == current_user.id).one()
    user_to_put.points -= int(POINTS_UPLOAD_COST)
    db.commit()

    if S3_response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return {
            "message": f"Image created with id: {image_model.id} with eloscore {elo_model.mu, elo_model.sigma}"
        }

    db.rollback()
    return {"message": f"Error uploading to S3 {S3_response}"}


@router.get("/images/votes", response_model=List[ImageSchema])
async def get_image_for_vote(db: Session = Depends(DBC.get_session)):
    """
    GET two images to vote on
    :param db: DB session
    :return: image paths and user ids
    """

    return [
        {
            "id": image.id,
            "user_id": image.user_id,
            "file": image.file,
            "created_at": image.created_at,
        }
        for image in db.query(ImageModel).order_by(func.random()).limit(2).all()
    ]


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
        return {
            "id": image.id,
            "user_id": image.user_id,
            "file": image.file,
            "created_at": image.created_at,
        }
    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"{image_id} does not exist")
