from fastapi import FastAPI

import strawberry
from strawberry.fastapi import GraphQLRouter

from app.graphql.core import Query, Mutation

#from fastapi.security import OAuth2

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

app = FastAPI()

app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
async def root():
    return {"message": "Hello World"}