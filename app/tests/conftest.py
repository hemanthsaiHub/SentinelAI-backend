import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..database.db import Base, get_db
from unittest.mock import patch

@pytest.fixture
def test_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    TestingSession = sessionmaker(bind=engine)
    yield TestingSession()
    Base.metadata.drop_all(engine)

@pytest.fixture
def db_session(test_db):
    return test_db
