import datetime

from app.tests import db
from alembic.config import Config
from alembic import command
from geoalchemy2.shape import shapely, from_shape

from app.models.user import User as UserModel
from app.auth import middleware

class TestMeeting():
    def setup_class(self):

        alembic_cfg = Config("alembic.ini")
        # alembic_cfg.set_main_option()
        alembic_cfg.set_main_option("is_testing", "True")
        alembic_cfg.set_main_option('sqlalchemy.url', db.SQLALCHEMY_TEST_DATABASE_URL)
        print(db.SQLALCHEMY_TEST_DATABASE_URL)
        command.upgrade(alembic_cfg, "head")


        self.test_sess = db.TestSessionLocal()
        print("sess")

        # Base.metadata.create_all(engine)
        # self.session = Session()
        self.password : str = "secret_pass"
        self.valid_author = Author(
            email = "mail@test.com",
            hashed_password = middleware.get_password_hash(password),
            first_name = "Tester",
            last_name = "Smith",


            location = from_shapeshapely.geomtry.Point(),
            location_update_datedatetime = datetime.datetime.utcnow(),

        )


    def test_seeking_people_around(self):
        print(f"Querry {self.test_sess.query(UserModel).all()}")
    
    def teardown_class(self):
        # self.session.rollback()
        # self.session.close()
        pass