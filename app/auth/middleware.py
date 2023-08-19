from functools import cached_property

from typing import Any
from passlib.context import CryptContext
from strawberry.permission import BasePermission
from strawberry.types import Info
from strawberry.fastapi import BaseContext

from app.db.database import SessionLocal
from app.models.user import User as UserModel
from app.auth.jwt import verify_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

class IsAuthenticated(BasePermission):
    message = "User is not authenticated"
    
    def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
        request: Union[Request, WebSocket] = info.context["request"]
        
        print(request.headers)
        if "Authorization" in request.headers:
            print(request.headers['Authorization'])
            user_db = verify_token( request.headers['Authorization'][7:] )
            if user_db:
                return True

        return False


class Context(BaseContext):
    @cached_property
    def user(self) -> UserModel | None:
        if not self.request:
            return None

        authorization = self.request.headers.get('Authorization', None)
        
        
        user_db = isinstance(authorization, str) and verify_token( authorization[7:] )

        return user_db or None

def get_context() -> Context:
    return Context()

