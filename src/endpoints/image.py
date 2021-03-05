from typing import List
import sqlalchemy
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from ..schemas.images import ImageSchema, ImageCreate, ImageDelete, ImageUpdate
from ..orm_models.db_models import ImageModel
from . import DBC

router = APIRouter()


@router.get("/images", response_model=List[ImageSchema])
def get_all_images(db: Session = Depends(DBC.get_session)):
    """
    GET all images
    :param db: DB session
    :return: ALl image entries
    """
    return [{"id": image.id,
             "user_id": image.user_id,
             "file": image.file
             "created_at": image.created_at} for image in db.query(ImageModel).all()]


@router.get("/images/name/{image_name}", response_model=ImageSchema)
def get_one_image_by_name(image_name: str, db: Session = Depends(DBC.get_session)):
    """
    GET one image by name
    :param image_name: Image name to get
    :param db: DB session
    :return: Retrieved image entry
    """
    try:
        # Get image by name
        image = db.query(ImageModel).filter(ImageModel.name == image_name).one()
        return {"id": image.id,
                "user_id": image.user_id,
                "file": image.file
                "created_at": image.created_at}
    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"{image_name} does not exist")


@router.get("/images/id/{image_id}", response_model=ImageSchema)
def get_one_image_by_id(image_id: str, db: Session = Depends(DBC.get_session)):
    """
    GET one image by ID
    :param image_id: Image ID to get
    :param db: DB session
    :return: Retrieved image entry
    """
    try:
        # Get image by name
        image = db.query(ImageModel).filter(ImageModel.id == image_id).one()
        return {"id": image.id,
                "user_id": image.user_id,
                "file": image.file
                "created_at": image.created_at}
    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"{image_id} does not exist")


@router.post("/images", response_model=ImageSchema)
def post_one_image(image: ImageCreate, db: Session = Depends(DBC.get_session)):
    """
    POST one image
    It reads parameters from the request field and add missing fields from default values defined in the model
    :param image: ImageBase class that contains all columns in the table
    :param db: DB session
    :return: Created image entry
    """
    image_to_create = ImageModel(**vote.dict())

    # Commit to DB
    db.add(vote_to_create)
    db.commit()
    db.refresh(vote_to_create)


@router.put("/images", response_model=ImageSchema)
def put_one_image(image: ImageUpdate, db: Session = Depends(DBC.get_session)):
    """
    PUT one image
    It reads parameters from the request field and update finds the entry and update it
    :param image: ImageUpdate class that contains requested field to update
    :param db: DB session
    :return: Updated image entry
    """
    try:
        # Get image by ID
        image_to_put = db.query(ImageModel).filter(ImageModel.id == image.id).one()

        # Update model class variable for requested fields
        for var, value in vars(image).items():
            setattr(image_to_put, var, value) if value else None

        # Commit to DB
        db.add(image_to_put)
        db.commit()
        return {"id": image.id,
                "user_id": image.user_id,
                "file": image.file
                "created_at": image.created_at}
    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"{image.id} does not exist")


@router.delete("/images/id/{image_id}", response_model=ImageDelete)
def delete_one_image_by_id(image_id: str, db: Session = Depends(DBC.get_session)):
    """
    DELETE one image by ID
    It reads parameters from the request field, finds the entry and delete it
    :param image_id: Image ID to delete
    :param db: DB session
    :return: Deleted image entry
    """
    try:
        # Delete entry
        affected_rows = db.query(ImageModel).filter(ImageModel.id == image_id).delete()
        if not affected_rows:
            raise sqlalchemy.orm.exc.NoResultFound
        # Commit to DB
        db.commit()
        return {"id": image.id}
    except sqlalchemy.orm.exc.NoResultFound:
        raise Exception(f"{image_id} does not exist")
