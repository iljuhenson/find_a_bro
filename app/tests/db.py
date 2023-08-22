import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool

SQLALCHEMY_TEST_DATABASE_URL = f"{os.getenv('TEST_DB_ENGINE')}://{os.getenv('TEST_DB_USER')}:{os.getenv('TEST_DB_PASSWORD')}@{os.getenv('TEST_DB_HOST')}:{os.getenv('TEST_DB_PORT')}/{os.getenv('TEST_DB_NAME')}"
test_engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, poolclass=NullPool)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
