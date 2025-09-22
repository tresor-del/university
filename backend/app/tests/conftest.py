from fastapi import BackgroundTasks
import pytest

from fastapi.testclient import TestClient

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, Session

from app.main import app
from app.models.students import Student
from app.models.teachers import Teacher
from app.models.media import Media
from app.models import users
from app.core.config import Base
from app.core.settings import settings
from app.api.deps import get_db
from app.initial_data import init_db
from app.tests.utils.users import authenticate_user_from_username
from app.tests.utils.utils import get_superuser_token_headers


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """
    Crée les tables, initialise la base de donnée avec le superuser.
    Supprime les tables à la fin. 
    """
    Base.metadata.create_all(bind=engine)  
    with Session(engine) as session:
        init_db(session)  
        session.commit()
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db():
    """
    Ouvre une session pour le test
    Après le test, nettoie les données crées sauf pour les users
    """
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.query(Student).delete() 
        session.query(Teacher).delete() 
        session.query(Media).delete()
        session.commit()
        session.close()

@pytest.fixture(scope="function")   
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="function")
def superuser_token_headers(client: TestClient) -> dict[str, str]:
    return get_superuser_token_headers(client)

@pytest.fixture(scope="function")
def bgtasks():
    return BackgroundTasks()

@pytest.fixture(scope="function")
def normal_user_token_headers(client: TestClient, db: Session):
    headers = authenticate_user_from_username(
        client=client,
        username=settings.USERNAME_TEST_USER,
        db=db
    )
    
    yield headers 
    
    # Supprimer l'utilisateur test pour eviter les conflits lors des prochains tests
    statement = select(users.User).where(users.User.username==settings.USERNAME_TEST_USER)
    user = db.execute(statement=statement).scalar_one_or_none()
    if user:
        db.delete(user)
        db.commit()