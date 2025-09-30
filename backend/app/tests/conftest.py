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
from app.schemas.university import CourseCreate, DepartmentCreate, FacultyCreate, ProgramCreate
from app.crud import programs, departements, courses, faculty 


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

@pytest.fixture(scope="function")
def setup_university_data(db: Session):
    """
    Fixture pour peupler la base de données avec des données de test.
    """

    # 1. Créer une faculté
    faculty1 = faculty.create_faculty(db=db, faculty_data=FacultyCreate(nom="Sciences et Technologies"))

    # 2. Créer un département lié à la faculté
    
    d = DepartmentCreate(nom="Informatique", id_faculte=str(faculty1.id))
    
    department1 = departements.create_departement(db=db, departement_data=d)

    # 3. Créer un programme (parcours) lié au département
    
    data = ProgramCreate(
        nom="Génie Logiciel",
        description="Apprenez à construire des logiciels robustes.",
        niveau="Licence",
        duree=3,
        id_departement=str(department1.id)
    )
    
    program1 = programs.create_program(db=db, data=data)

    # 4. Créer un cours lié au programme
    
    cours_data = CourseCreate(
        titre="Algorithmique",
        description="Bases de l'algorithmique.",
        code="CS101",
        credits=5,
        id_parcours=str(program1.id)
    )
    
    course1 = courses.create_course(db=db, data=cours_data)
    
    return {
        "program": program1,
        "department": department1,
        "course": course1
    }
