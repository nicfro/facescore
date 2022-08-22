import os
import sys
import base64
import json
import requests
from typing import List, Tuple


sys.path.insert(0, os.getcwd())

import sqlalchemy
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException, status
from src.schemas.images import ImageSchema, ImageCreateRequest, ImageCreateResponse
from src.schemas.users import UserSchema
from src.orm_models.db_models import ImageModel, EloModel
from . import DBC, S3
from src.logic.hasher import Hasher
from src.logic.auth import get_current_user_db
from src.settings import load_config
from src.logic.distances import cosine

hasher = Hasher()
router = APIRouter()

if os.path.isfile("ENV"):
    load_config("ENV")

POINTS_UPLOAD_COST = os.environ.get("POINTS_UPLOAD_COST")
ML_ENDPOINT = os.environ.get("ML_ENDPOINT")
IMAGE_VERIFICATION_THRESHOLD = float(os.environ.get("IMAGE_VERIFICATION_THRESHOLD"))


def forbidden_exception(reason):
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"{reason}",
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.post("/images", response_model=ImageCreateResponse)
async def post_image(
    image: ImageCreateRequest,
    current_user_db: Tuple[UserSchema, Session] = Depends(get_current_user_db),
):
    """
    POST one image to database if sucessful also to S3
    Gets user_id & Gender from form and file as an UploadFile object
    :param user_id: the user id of the image
    :param file: the file to be uploaded
    :param db: DB session
    :return: Created image entry
    """
    current_user, db = current_user_db
    if current_user.points < 10:
        return forbidden_exception("Not enough points for image upload")

    if not current_user.verified:
        return forbidden_exception("User is not verified")

    headers = {"Content-type": "application/json", "Accept": "text/plain"}
    payload = json.dumps({"image": image.image})
    response = requests.post(
        ML_ENDPOINT + "detections/embedding", data=payload, headers=headers
    )

    if not response.status_code == 200:
        raise forbidden_exception(response.json()["detail"])

    data = response.json()
    embedding = data["embedding"]

    if not (
        cosine(embedding, current_user.embedding1) > IMAGE_VERIFICATION_THRESHOLD
    ) and (cosine(embedding, current_user.embedding2) > IMAGE_VERIFICATION_THRESHOLD):
        raise forbidden_exception("Cannot verify the uploaded picture")

    # Store image in S3
    image_name = f"images/{current_user.gender}/{hasher.image_hash(image.image)}"

    S3_response = S3.upload_image(image.image, image_name)
    if S3_response["ResponseMetadata"]["HTTPStatusCode"] != 200:
        raise forbidden_exception(
            f"Error with uploading the image to S3: {S3_response}"
        )

    image_args = {"user_id": current_user.id, "file": image_name}
    image_model = ImageModel(**image_args)
    db.add(image_model)
    db.flush()

    elo_args = {"image_id": image_model.id}
    elo_model = EloModel(**elo_args)

    db.add(elo_model)
    current_user.points += int(POINTS_UPLOAD_COST)
    db.commit()

    return ImageCreateResponse(
        image_id=image_model.id, elo_mu=elo_model.mu, elo_sigma=elo_model.sigma
    )


@router.get("/images/votes", response_model=List[ImageSchema])
async def get_images_for_vote(db: Session = Depends(DBC.get_session)):
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
