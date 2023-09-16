import typing
import strawberry
from app.models.user import User as UserModel
from typing import List

@strawberry.type
class User:
    id: strawberry.ID    
    email: str
    hashed_password: str
    first_name: str
    last_name: str
    description: str
    profile_picture_path: str
    is_active: bool
    
    @classmethod
    def marshal(cls, userModel: UserModel) -> typing.Self:
        return cls(
            id=strawberry.ID(str(userModel.id)),
            email=userModel.email, 
            hashed_password=userModel.hashed_password,
            first_name=userModel.first_name, 
            last_name=userModel.last_name,
            description=userModel.description,
            profile_picture_path=userModel.profile_picture_path,
            is_active=userModel.is_active
        )

@strawberry.type
class AuthenticationError:
    message: str

@strawberry.type
class AccessToken:
    token: str

    @classmethod
    def marshal(cls, access_token: str):
        return cls(token=access_token)

@strawberry.type
class UserList:
    users: List[User]


@strawberry.type
class TargetMeetingUserError:
    message: str
