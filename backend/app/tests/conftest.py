import pytest
from fastapi.testclient import TestClient

from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import students
from app.models.students import Base


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback() 
        connection.close()
        Base.metadata.drop_all(bind=engine) 


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

