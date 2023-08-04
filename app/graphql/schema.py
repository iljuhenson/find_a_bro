import typing
import strawberry
from app.models.user import User as UserModel

@strawberry.type
class User:
    id: strawberry.ID    
    email: str
    password: str
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
            password=userModel.password,
            first_name=userModel.first_name, 
            last_name=userModel.last_name,
            description=userModel.description,
            profile_picture_path=userModel.profile_picture_path,
            is_active=userModel.is_active
        )