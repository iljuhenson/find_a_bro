from typing import List
from fastapi import HTTPException, status
from strawberry.exceptions import InvalidArgumentTypeError

from app.auth.middleware import verify_password, get_password_hash
from app.db.database import SessionLocal
from app.models.user import User as UserModel
from app.graphql.schema import User as UserType, AccessToken as AccessTokenType
from app.graphql.inputs import UserSignUpInput
from app.auth.jwt import create_access_token

class User:
    def get_users(self) -> List[UserType]:
        users = SessionLocal().query(UserModel).all()
        return list(map(lambda user: UserType.marshal(user), users))
        
    def create_user(self, user: UserSignUpInput) -> UserType:
        sess = SessionLocal()
        user_db = UserModel(email=user.email, hashed_password=get_password_hash(user.password), first_name=user.first_name, last_name=user.last_name)
        sess.add(user_db)
        sess.commit()
        return UserType.marshal(user_db)

    def login(self, email: str, password: str) -> AccessTokenType:
        sess = SessionLocal()
        
        user_db = sess.query(UserModel).filter(UserModel.email == email).first()
        if not user_db:
            raise Exception("User doesn't exist")
        elif not verify_password(password, user_db.hashed_password):
            raise Exception("Wrong password was specified")
        else:
            access_token = create_access_token(user_db)
            return AccessTokenType.marshal(access_token)