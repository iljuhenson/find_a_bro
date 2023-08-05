from typing import Annotated
from app.db.database import SessionLocal
from app.models.user import User as UserModel

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def decode_token(token: str) -> dict:
    pass

def get_user_model(token: str):
    user_metadata = decode_token(token)
    return SessionLocal().querry(UserModel).get(user_metadata.id)