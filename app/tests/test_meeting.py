import os
import datetime
from unittest.mock import patch

from starlette.requests import Request
from starlette.datastructures import Headers
from fastapi.testclient import TestClient
from alembic.config import Config
import alembic
from geoalchemy2.shape import from_shape
from shapely import Point
from sqlalchemy.orm import close_all_sessions
from sqlalchemy.orm import sessionmaker
import requests
import pytest
import uvicorn
from app.main import schema

from app.tests import db
from app.db import database
from app.db.database import Base
from app.models.user import User as UserModel
from app.auth import middleware
from app.main import app


# Needs change probably
from strawberry.fastapi import BaseContext
from functools import cached_property
from app.auth.jwt import verify_token



locations = [
    #            lat                  lon
    Point(52.2256918356944,   20.980238913180077),
    Point(52.224692883909185, 20.97908878247836),
    Point(52.17305001104562,  21.110263810842298),
    Point(52.17079704474586,  20.99288177385461),
]


class CustomContext(BaseContext):

    @cached_property
    def user(self) -> UserModel | None:
        # print("I'm logging")
        if not self.request:
            return None

        print(self.request.headers.get('Authorization'))
        authorization = self.request.headers.get('Authorization', None)
        
        print(f"auth: {authorization}")
        user_db = isinstance(authorization, str) and verify_token( authorization[7:], next(self.get_db()) )

        print(f"user db: {user_db}")
        return user_db or None
    
    def get_db(self):
        return db.get_test_db()

class TestMeeting():

    def setup_class(self):
                
        alembic_cfg = Config("alembic.ini")
        alembic_cfg.set_main_option("is_testing", "True")
        alembic.command.upgrade(alembic_cfg, "head")

        self.test_sess = next(db.get_test_db())

        for c in Base.registry._class_registry.values():
            if hasattr(c, '__tablename__'):
                self.test_sess.query(c).delete()
                print(f"class: {c}")
        self.password : str = "secret_pass"
        # self.test_sess = db.TestSessionLocal()

        self.main_user = UserModel(
            email = "mail@test.com",
            hashed_password = middleware.get_password_hash(self.password),
            first_name = "Tester",
            last_name = "Smith",      # 52.2256918356944,   20.980238913180077
            location = from_shape(Point(52.2256918356944,   20.980238913180077)),
            location_update_date = datetime.datetime.utcnow(),
        )
        
        self.test_sess.add(self.main_user)
        self.custom_context = CustomContext()


    def test_seeking_people_around(self):
        users = []
        # print(res)
        # print("im in test")
        # self.test_sess.add(self.main_user)
        # print("I added to session")
        for i in range(len(locations)):
            # print("while location loop")

            temp = UserModel(
                email = f"mail{i}@test.com",
                hashed_password = middleware.get_password_hash(self.password),
                first_name = f"Tester{i}",
                last_name = f"Smith{i}",
                location = from_shape(locations[i]),
                location_update_date = datetime.datetime.utcnow(),
            )
            
            users.append(temp)
            self.test_sess.add(temp)
        try:
            self.test_sess.commit()
            print(self.test_sess.query(UserModel).all())
            testing_query = '''query GetProfilesAdminovich {
                            getProfilesWithin(distance: 2) {
                                ... on User {
                                id
                                email
                                }
                                ... on AuthenticationError {
                                __typename
                                }
                            }
                            }'''
            jwt_querry = '''query LoginAdminovich {
                login(email: "%s", password: "%s") {
                    token
                }
            }''' % (self.main_user.email, self.password) #  ("admin@admin.com", "pass.123") 

            jwt_token_response = schema.execute_sync(query=jwt_querry, context_value=self.custom_context)
            graphql_link = "/graphql"
            
            print(jwt_token_response)
            jwt_token = jwt_token_response.data['login']['token']

            headers={"Authorization" : f"Bearer {jwt_token}"}
            r = Request(scope={
                "type": "http",
                "headers": Headers(headers).raw,
            })

            self.custom_context.request = r 
            response = schema.execute_sync(query=testing_query, context_value=self.custom_context)
            # response = self.client.post(graphql_link, json={'query': testing_query}, headers={"Authentication" : f"Bearer {jwt_token}"})
            print(response)
            response_body = response.data
            print(response_body)
            # print("query end")
        except:
            self.test_sess.rollback()
            raise

        
    
    def teardown_class(self):
        print("Deleting data")
        # # self.test_sess.rollback()
        for c in Base.registry._class_registry.values():
            if hasattr(c, '__tablename__'):
                self.test_sess.query(c).delete()
                print(f"class: {c}")
        
        # self.test_sess.commit()
        
        print("Data deleted")
        # self.test_sess.close()