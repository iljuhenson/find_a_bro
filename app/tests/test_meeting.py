import datetime
from unittest.mock import patch

from alembic.config import Config
from alembic import command
from geoalchemy2.shape import from_shape
from shapely import Point
from sqlalchemy.orm import close_all_sessions
from sqlalchemy.orm import sessionmaker
import requests
import pytest

from app.tests import db
from app.db import database
from app.db.database import Base
from app.models.user import User as UserModel
from app.auth import middleware


locations = [
    #            lat                  lon
    Point(52.2256918356944,   20.980238913180077),
    Point(52.224692883909185, 20.97908878247836),
    Point(52.17305001104562,  21.110263810842298),
    Point(52.17079704474586,  20.99288177385461),
]


class TestMeeting():
    # def __init__(self):
    #     self.test_sess = None

    @pytest.fixture(autouse=True)
    def no_delay(self):
        with patch('app.db.database.SessionLocal', return_value=db.TestSessionLocal()):
            yield

    def setup_class(self):

        # database.change_session_local(db.TestSessionLocal)        
        # print("Deleting data")
        # Base.metadata.drop_all(bind=db.test_engine)
        # # meta = Base.metadata
        # # self.test_sess.rollback()
        # # for table in reversed(meta.sorted_tables):
        # #     print('Clear table %s' % table)
        # #     self.test_sess.execute(table.delete())
        # # self.test_sess.commit()
        # print("Data deleted")
        # close_all_sessions()
        Base.metadata.create_all(bind=db.test_engine)
        # print("migrating with alembic")
        alembic_cfg = Config("alembic.ini")
        # alembic_cfg.set_main_option()
        alembic_cfg.set_main_option("is_testing", "True")
        alembic_cfg.set_main_option('sqlalchemy.url', db.SQLALCHEMY_TEST_DATABASE_URL)
        print(db.SQLALCHEMY_TEST_DATABASE_URL)
        command.upgrade(alembic_cfg, "head")

        print(Base.metadata.tables.values())
        print("classdecl")


        self.password : str = "secret_pass"
        self.test_sess = db.TestSessionLocal()

        self.main_user = UserModel(
            email = "mail@test.com",
            hashed_password = middleware.get_password_hash(self.password),
            first_name = "Tester",
            last_name = "Smith",
            # location = from_shape(Point(52.225350091660424, 20.9785737983475)),
            # location_update_date = datetime.datetime.utcnow(),
        )


    def test_seeking_people_around(self):
        users = []
        print("im in test")
        self.test_sess.add(self.main_user)
        print("I added to session")
        for i in range(len(locations)):
            print("while location loop")

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
            
            print("requesting")
            print(f"Querry {self.test_sess.query(UserModel).all()}")
            graphql_link = "http://127.0.0.1:8000/graphql"
            jwt_querry = '''query LoginAdminovich {
                login(email: "%s", password: "%s") {
                    token
                }
            }''' % ("admin@admin.com", "pass.123") # (self.main_user.email, self.password) 
            

            jwt_token_response = requests.post(graphql_link, json={'query': jwt_querry})
            print(jwt_querry)
            print(f"debug token_response: {jwt_token_response.json()}")
            jwt_token = jwt_token_response.json()['data']['login']['token']

            response = requests.post(graphql_link, json={'query': testing_query}, headers={"Authentication" : f"Bearer {jwt_token}"})
            response_body = response.json()
            print(response_body)
            print("query end")
        except:
            self.test_sess.rollback()
            raise

        
    
    def teardown_class(self):
        print("Deleting data")
        # self.test_sess.rollback()
        for c in Base.registry._class_registry.values():
            if hasattr(c, '__tablename__'):
                self.test_sess.query(c).delete()
                print(f"class: {c}")
        
        self.test_sess.commit()
        
        print("Data deleted")
        self.test_sess.close()