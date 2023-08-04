from typing import Annotated
from app.db.database import SessionLocal
from app.models.user import User as UserModel

def decode_token(token: str) -> dict:
    pass

def get_user_model(token: Annotated[str, ]):
    user_metadata = decode_token(token)
    return SessionLocal().querry(UserModel).get(user_metadata.id)