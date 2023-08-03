import strawberry

@strawberry.type
class Query:
    @strawberry.field
    def get_all_users():
        pass

@strawberry.type
class Mutation:
    pass