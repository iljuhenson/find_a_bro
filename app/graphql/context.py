from strawberry.fastapi import BaseContext
from functools import cached_property
from app.models.user import User as UserModel
from app.auth.jwt import verify_token
from app.db.database import get_db


class Context(BaseContext):
    @cached_property
    def user(self) -> UserModel | None:
        # print("I'm logging")
        if not self.request:
            return None

        # print("request is not none")
        authorization = self.request.headers.get('Authorization', None)
        
        # print(f"auth: {authorization}")
        user_db = isinstance(authorization, str) and verify_token( authorization[7:], next(self.get_db()) )

        # print(f"user db: {user_db}")
        return user_db or None
    
    def get_db(self):
        return get_db()

    

def get_context() -> Context:
    return Context()