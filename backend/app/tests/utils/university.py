from typing import List
import uuid
from uuid import UUID
from sqlalchemy.orm import Session

from app.crud.admin.courses import  create_course
from app.crud.admin.departements import create_departement
from app.models.university import Program, Faculty
from app.schemas.university import CourseCreate, CourseResponse, ProgramCreate, FacultyCreate, FacultyResponse, DepartmentCreate, ProgramResponse
from app.tests.utils.utils import random_lower_string

def create_random_faculty(db: Session) -> FacultyResponse:
    data = FacultyCreate(
        nom=random_lower_string(),
        description=random_lower_string(),
    )
    faculty = Faculty(**data.model_dump())
    db.add(faculty)
    db.commit()
    db.refresh(faculty)
    return FacultyResponse.model_validate(faculty)

def create_random_faculties(db: Session, n: int = 3) -> list[FacultyResponse]:
    faculties = []
    for _ in range(n):
        faculties.append(create_random_faculty(db))
    return faculties

def create_random_program(db: Session, id_departement: UUID = uuid.uuid4()) -> Program:
    """Crée un programme aléatoire pour rattacher les cours."""
    data = ProgramCreate(
        nom=random_lower_string(),
        niveau="Licence",
        duree=3,
        id_departement=id_departement, 
        description="Programme test"
    )
    program = Program(**data.model_dump())
    db.add(program)
    db.commit()
    db.refresh(program)
    return program


def create_random_course(db: Session, program_id: UUID = uuid.uuid4()) -> CourseResponse:
    """Crée un cours aléatoire avec un programme lié."""
    data = CourseCreate(
        code=random_lower_string(),
        titre=random_lower_string(),
        description=random_lower_string(),
        credits=4,
        id_parcours=program_id,
    )
    return create_course(db=db, data=data)


def create_random_courses(db: Session, n: int = 3) -> list[CourseResponse]:
    courses = []
    for _ in range(n):
        courses.append(create_random_course(db))
    return courses


def create_random_department(db: Session, faculty_id: UUID):
    data = DepartmentCreate(
        nom=random_lower_string(),
        description=random_lower_string(),
        id_faculte=faculty_id,
    )
    return create_departement(db=db, departement_data=data)

def create_random_departements(db: Session,n: int = 3, faculty_id: UUID = None) -> list:
    departements = []
    for _ in range(n):
        departements.append(create_random_department(db,faculty_id=faculty_id or uuid.uuid4()))
    return departements

def create_random_programs(db: Session, n: int = 3, id_departement: UUID = None) -> List[Program]:
    programs = []
    for _ in range(n):
        programs.append(create_random_program(db, id_departement=id_departement or uuid.uuid4()))
    return programs

def get_random_program(db: Session, program_id: UUID) -> ProgramResponse | None:
    from app.crud.admin.programs import get_program
    return get_program(db=db, program_id=program_id)