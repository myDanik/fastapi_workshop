import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..database import get_db_session
from ..tables import Base, User, Operation
from dotenv import load_dotenv
import os

load_dotenv() 

@pytest.fixture(scope="session")
def engine():
    return create_engine(f"{os.getenv('TEST_DATABASE_URL')}")

@pytest.fixture(scope="session")
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture
def session(engine, tables):
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def test_user(session):
    user = User(email="test@example.com", username="testuser", password_hash="hash")
    session.add(user)
    session.commit()
    return user