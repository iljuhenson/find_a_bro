from typing import Optional
import strawberry
from strawberry.types import Info as _Info
from strawberry.types.info import RootValueType
from app.graphql.context import Context

@strawberry.input
class UserSignUpInput:    
    email: str
    password: str
    first_name: str
    last_name: str

Info = _Info[Context, RootValueType]