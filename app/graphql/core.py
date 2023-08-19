from typing import Annotated, Union, List, AsyncGenerator
import strawberry
from strawberry.type import Union as _Union

from . import controllers
from app.auth.middleware import IsAuthenticated


from .schema import User, AccessToken, AuthenticationError

@strawberry.type
class Query:
    users: List[User] = strawberry.field(resolver=controllers.User.get_users, permission_classes=[IsAuthenticated])
    login: AccessToken = strawberry.field(resolver=controllers.User.login)
    get_profiles_within: _Union[User, AuthenticationError] = strawberry.field(resolver=controllers.Meeting.get_profiles_within)


@strawberry.type
class Mutation:
    create_user: User = strawberry.mutation(resolver=controllers.User.create_user)

@strawberry.type
class Subscription:
    pass