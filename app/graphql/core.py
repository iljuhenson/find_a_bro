from typing import List
import strawberry

from . import controllers
from app.auth.middleware import IsAuthenticated

from .schema import User, AccessToken

@strawberry.type
class Query:
    users: List[User] = strawberry.field(resolver=controllers.User.get_users, permission_classes=[IsAuthenticated])
    login: AccessToken = strawberry.field(resolver=controllers.User.login)


@strawberry.type
class Mutation:
    create_user: User = strawberry.mutation(resolver=controllers.User.create_user)