from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, VARCHAR, TIMESTAMP, ForeignKey, Integer, PrimaryKeyConstraint, VARBINARY, Date
from sqlalchemy.sql import func

BaseModel = declarative_base()


class UserModel(BaseModel):
    """
    Define Users database table ORM model
    """
    __tablename__ = "users"

    # Register columns
    id = Column(Integer, unique=True, primary_key=True, index=True, autoincrement=True)
    name = Column(VARCHAR, index=True)
    email = Column(VARCHAR, unique=True, index=True)
    gender = Column(VARCHAR, index=True)
    country = Column(VARCHAR, index=True)
    birthdate = Column(Date, unique=True, index=True)
    hashed_password = Column(VARCHAR, unique=True, index=True)
    salt = Column(VARCHAR, unique=True, index=True)
    PrimaryKeyConstraint(id, name="PK_users_id")


class ImageModel(BaseModel):
    """
    Define Images database table ORM model
    """
    __tablename__ = "images"

    # Register columns
    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    user_id = Column(Integer, unique=True)
    created_at = Column(TIMESTAMP, default=func.now())
    file = Column(VARBINARY)

    PrimaryKeyConstraint(id, name="PK_images_id")


class VoteModel(BaseModel):
    """
    Define Votes database table ORM model
    """
    __tablename__ = "votes"

    # Register columns
    id = Column(Integer, unique=True, primary_key=True, index=True, autoincrement=True)
    user_id = Column(ForeignKey("users.id", name="FK_votes_user_id_users_id"))
    left_image_id = Column(ForeignKey("images.id", name="FK_votes_left_image_id_images_id"))
    right_image_id = Column(ForeignKey("images.id", name="FK_votes_right_image_id_images_id"))
    file = Column(Binary())

    PrimaryKeyConstraint(id, name="PK_votes_id")

class EloModel(BaseModel):
    """
    Define Votes database table ORM model
    """
    __tablename__ = "elo"

    # Register columns
    id = Column(Integer, unique=True, primary_key=True, index=True, autoincrement=True)
    image_id = Column(ForeignKey("images.id", name="FK_elo_image_id_images_id"))
    score = Column(Integer())
    created_at = Column(TIMESTAMP, default=func.now())

    PrimaryKeyConstraint(id, name="PK_elo_id")