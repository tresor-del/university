import uuid
from sqlalchemy.orm import Session

from app.crud.courses import  create_course
from app.models.university import Program, Faculty
from app.schemas.university import CourseCreate, CourseResponse, ProgramCreate, FacultyCreate, FacultyResponse
from app.tests.utils.utils import random_lower_string

def create_random_faculty(db: Session):
    data = FacultyCreate(
        nom=random_lower_string(),
        description=random_lower_string(),
    )
    faculty = Faculty(**data.model_dump())
    db.add(faculty)
    db.commit()
    db.refresh(faculty)
    return faculty

def create_random_faculties(db: Session, n: int = 3) -> list[FacultyResponse]:
    faculties = []
    for _ in range(n):
        faculties.append(create_random_faculty(db))
    return faculties

def create_random_program(db: Session) -> Program:
    """Crée un programme aléatoire pour rattacher les cours."""
    data = ProgramCreate(
        nom=random_lower_string(),
        niveau="Licence",
        duree=3,
        id_departement=uuid.uuid4(), 
        description="Programme test"
    )
    program = Program(**data.model_dump())
    db.add(program)
    db.commit()
    db.refresh(program)
    return program


def create_random_course(db: Session) -> CourseResponse:
    """Crée un cours aléatoire avec un programme lié."""
    program = create_random_program(db)
    data = CourseCreate(
        code=random_lower_string(),
        titre=random_lower_string(),
        description=random_lower_string(),
        credits=4,
        id_parcours=program.id,
    )
    return create_course(db=db, data=data)


def create_random_courses(db: Session, n: int = 3) -> list[CourseResponse]:
    courses = []
    for _ in range(n):
        courses.append(create_random_course(db))
    return courses
