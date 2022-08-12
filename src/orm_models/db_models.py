from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, VARCHAR, TIMESTAMP, ForeignKey, Integer, Date, Float
from sqlalchemy.sql import func


BaseModel = declarative_base()


class UserModel(BaseModel):
    """
    Define Users database table ORM model
    """

    __tablename__ = "users"

    # Register columns
    id = Column(Integer, index=True, unique=True, autoincrement=True, primary_key=True)
    name = Column(VARCHAR(length=255), index=True, unique=True)
    email = Column(VARCHAR(length=255), index=True, unique=True)
    gender = Column(VARCHAR(length=255), nullable=True)
    country = Column(VARCHAR(length=255), nullable=True)
    birthdate = Column(Date, index=True, nullable=True)
    hashed_password = Column(VARCHAR(length=255))
    salt = Column(VARCHAR(length=255))
    created_at = Column(TIMESTAMP, default=func.now())


class ImageModel(BaseModel):
    """
    Define Images database table ORM model
    """

    __tablename__ = "images"

    # Register columns
    id = Column(Integer, unique=True, autoincrement=True, primary_key=True)
    user_id = Column(
        ForeignKey("users.id", name="FK_images_user_id_user_id", ondelete="CASCADE")
    )
    file = Column(VARCHAR(length=255), unique=True)
    created_at = Column(TIMESTAMP, default=func.now())


class VoteModel(BaseModel):
    """
    Define Votes database table ORM model
    """

    __tablename__ = "votes"

    # Register columns
    id = Column(Integer, unique=True, index=True, autoincrement=True, primary_key=True)
    user_id = Column(
        ForeignKey("users.id", name="FK_votes_user_id_users_id", ondelete="CASCADE")
    )

    winner_image_id = Column(
        ForeignKey("images.id", name="FK_winner_image_id_images_id", ondelete="CASCADE")
    )
    loser_image_id = Column(
        ForeignKey("images.id", name="FK_loser_image_id_images_id", ondelete="CASCADE")
    )

    created_at = Column(TIMESTAMP, default=func.now())


class EloModel(BaseModel):
    """
    Define Votes database table ORM model
    """

    __tablename__ = "elo"

    # Register columns
    id = Column(Integer, unique=True, index=True, autoincrement=True, primary_key=True)
    image_id = Column(
        ForeignKey("images.id", name="FK_elo_image_id_images_id", ondelete="CASCADE")
    )
    mu = Column(Float, default=25)
    sigma = Column(Float, default=8.33)
    created_at = Column(TIMESTAMP, default=func.now())


class ModelOrder:
    tables = [UserModel, ImageModel, VoteModel, EloModel]
