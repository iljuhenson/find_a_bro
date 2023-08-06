from datetime import datetime, timedelta
from jose import jwt 
from app.models.user import User as UserModel
from app.db.database import SessionLocal

SECRET_KEY = "1384127959782783e4176c56da1bb5782bef102c1b8f0f64bb3bb1285523108c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(user: UserModel, expires_after_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    to_encode = {
        "id": user.id,
        "email": user.email,
        "exp": datetime.utcnow() + timedelta(minutes=expires_after_minutes),
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> UserModel:
    sess = SessionLocal()
    
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
    user_db = sess.query(UserModel).filter(UserModel.email == payload['email'] and UserModel.id == payload['id']).first()

    return user_db
        