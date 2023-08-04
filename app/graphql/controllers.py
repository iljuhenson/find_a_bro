from typing import List
from app.db.database import SessionLocal
from app.models.user import User as UserModel
from app.graphql.schema import User as UserType
from app.graphql.inputs import UserSignUpInput

class User:
    def get_users(self) -> List[UserType]:
        users = SessionLocal().query(UserModel).all()
        return list(map(lambda user: UserType.marshal(user), users))
        
    def create_user(self, user: UserSignUpInput) -> UserType:
        sess = SessionLocal()
        user_model_instance = UserModel(email=user.email, password=user.password, first_name=user.first_name, last_name=user.last_name)
        sess.add(user_model_instance)
        sess.commit()
        return UserType.marshal(user_model_instance)
