from pydantic import BaseModel


class TokenSchema(BaseModel):
    """
    Information on bestowed token
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Information on token
    """

    user_id: int | None = None
