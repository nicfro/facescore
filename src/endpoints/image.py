from typing import List
import sqlalchemy
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, UploadFile, File, Form
from ..schemas.images import ImageSchema, ImageCreate
from ..orm_models.db_models import ImageModel
from . import DBC
from src.logic.hasher import Hasher


router = APIRouter()
#, file: UploadFile = File(...)
@router.post("/uploadfile/")
async def post_image(user_id: str = Form(...), file: UploadFile = File(...), db: Session = Depends(DBC.get_session)):
    """
    POST one image
    It reads parameters from the request field and add missing fields from default values defined in the model
    :param user: ImageBase class that contains all columns in the table
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


