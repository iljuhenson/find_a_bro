import os
import datetime

from starlette.requests import Request
from starlette.datastructures import Headers
from alembic.config import Config
import alembic
from geoalchemy2.shape import from_shape
from shapely import Point
import pytest
from app.main import schema

from app.db.database import Base
from app.tests import db
from app.models.user import User as UserModel
from app.auth import middleware


# Needs change probably
from strawberry.fastapi import BaseContext
from functools import cached_property
from app.auth.jwt import verify_token



locations = [
    #            lat                  lon
    Point(50.672838, 21.047246),
    Point(50.673246, 21.046475),
    Point(50.658320, 21.024380),
    Point(50.657649, 21.026232),
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
                # print(f"class: {c}")
        self.password : str = "secret_pass"

        self.main_user = UserModel(
            email = "mail@test.com",
            hashed_password = middleware.get_password_hash(self.password),
            first_name = "Tester",
            last_name = "Smith",
            location = from_shape(Point(50.672784, 21.046689)),
            location_update_date = datetime.datetime.utcnow(),
        )
        
        self.test_sess.add(self.main_user)
        self.custom_context = CustomContext()


    def test_seeking_people_around(self):
        users = []
        
        for i in range(len(locations)):
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
            # print(self.test_sess.query(UserModel).all())
            testing_query = '''query GetProfilesAdminovich {
                            getProfilesWithin(distance: 2) {
                                ... on UserList {
                                __typename
                                    users {
                                        id
                                        email
                                    }
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
            }''' % (self.main_user.email, self.password)

            jwt_token_response = schema.execute_sync(query=jwt_querry, context_value=self.custom_context)
            graphql_link = "/graphql"
            
            jwt_token = jwt_token_response.data['login']['token']

            headers={"Authorization" : f"Bearer {jwt_token}"}
            r = Request(scope={
                "type": "http",
                "headers": Headers(headers).raw,
            })

            self.custom_context.request = r 
            response = schema.execute_sync(query=testing_query, context_value=self.custom_context)
            
            response_body = response.data
            
            assert len(response_body['getProfilesWithin']['users']) == 3

        except:
            self.test_sess.rollback()
            raise

        
    
    def teardown_class(self):
        print("Deleting data")
        for c in Base.registry._class_registry.values():
            if hasattr(c, '__tablename__'):
                self.test_sess.query(c).delete()
                # print(f"class: {c}")
        
        
        print("Data deleted")
        