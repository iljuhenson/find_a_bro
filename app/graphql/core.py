from typing import List
import strawberry

from app.graphql import controllers

from .schema import User

@strawberry.type
class Query:
    users: List[User] = strawberry.field(resolver=controllers.User.get_users)


@strawberry.type
class Mutation:
    create_user: User = strawberry.mutation(resolver=controllers.User.create_user)