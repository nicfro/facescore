from typing import List
import sqlalchemy
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, UploadFile, File, Form
from ..schemas.images import ImageSchema, ImageCreate
from ..orm_models.db_models import ImageModel
from . import DBC
from src.logic.hasher import Hasher
import base64


router = APIRouter()
#, file: UploadFile = File(...)
@router.post("/images")
async def post_image(user_id: int = Form(...), file: UploadFile = File(...), db: Session = Depends(DBC.get_session)):
    """
    POST one image
    Gets user_id from form and file as an UploadFile object
    :param user_id: the user id of the image
    :param file: the file to be uploaded
    :param db: DB session
    :return: Created image entry
    """
    image_args = {"user_id": user_id,
                  "file": file.file.read()}
    image_model = ImageModel(**image_args)
    
    # Commit to DB
    db.add(image_model)
    db.commit()
    db.refresh(image_model)
    return {"message": f"Image created with id: {image_model.id}"}


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
                "file": base64.b64encode(image.file), 
                "created_at": image.created_at}
    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"{image_id} does not exist")


