from typing import Union, List
from fastapi import HTTPException, status
from strawberry.exceptions import InvalidArgumentTypeError
import geoalchemy2 

from app.auth.middleware import verify_password, get_password_hash
from app.db.database import SessionLocal
from app.models.user import User as UserModel
from app.graphql.schema import User as UserType, AccessToken as AccessTokenType, AuthenticationError as AuthenticationErrorType, UserList as UserListType, Info
from app.graphql.inputs import UserSignUpInput
from app.auth.jwt import create_access_token


class User:
    def get_users(self, info: Info) -> List[UserType]:
        sess = next(info.context.get_db())
        users = sess.query(UserModel).all()
        return list(map(lambda user: UserType.marshal(user), users))
        
    def create_user(self, user: UserSignUpInput, info: Info) -> UserType:
        sess = next(info.context.get_db())
        user_db = UserModel(email=user.email, hashed_password=get_password_hash(user.password), first_name=user.first_name, last_name=user.last_name)
        sess.add(user_db)
        sess.commit()
        return UserType.marshal(user_db)

    def login(self, email: str, password: str, info: Info) -> AccessTokenType:
        sess = next(info.context.get_db())

        user_db = sess.query(UserModel).filter(UserModel.email == email).first()
        if not user_db:
            raise Exception("User doesn't exist")
        elif not verify_password(password, user_db.hashed_password):
            raise Exception("Wrong password was specified")
        else:
            access_token = create_access_token(user_db)
            return AccessTokenType.marshal(access_token)

class NotificationFeed:
    def subscribe_to_notifications(self):
        pass

class Meeting:
    def get_profiles_within(distance: int, info: Info):
        user = info.context.user

        if user is None:
            return AuthenticationErrorType(message="User is not logged in")
        # print("I'm in get profiles within")

        sess = next(info.context.get_db())
        # print(sess)
        users_within_db = sess.query(UserModel).filter(geoalchemy2.functions.ST_DWithin(UserModel.location, user.location, int(distance) * 1000))
        users_within = [UserType.marshal(userModel=user) for user in list(users_within_db)]

        user_list = UserListType(users=users_within)
        return user_list
