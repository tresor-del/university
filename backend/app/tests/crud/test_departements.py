from typing import Any, List
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud.departements import (
    read_departement,
    create_departement,
    update_departement,
    delete_department,
    get_departement,
)
from app.crud.courses import create_course
from app.schemas.university import (
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentResponse,
    FacultyCreate,
    ProgramCreate,
    CourseCreate,
    CourseResponse,
)
from app.models.university import Department, Program, Course, Faculty
from app.tests.utils.utils import random_lower_string


# Helpers
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


def create_random_department(db: Session, faculty_id: UUID):
    data = DepartmentCreate(
        nom=random_lower_string(),
        description=random_lower_string(),
        id_faculte=faculty_id,
    )
    return create_departement(db=db, departement_data=data)


def create_random_program(db: Session, department_id: UUID):
    data = ProgramCreate(
        nom=random_lower_string(),
        niveau="Licence",
        duree=3,
        id_departement=department_id,
        description="Programme test",
    )
    program = Program(**data.model_dump())
    db.add(program)
    db.commit()
    db.refresh(program)
    return program


def create_random_course(db: Session, program_id: UUID) -> CourseResponse:
    data = CourseCreate(
        code=random_lower_string(),
        titre=random_lower_string(),
        credits=4,
        id_parcours=program_id,
        description="Cours test",
    )
    return create_course(db=db, data=data)


# Tests CRUD Département + Relations

def test_create_department_with_relations(db: Session) -> Any:
    faculty = create_random_faculty(db)
    department = create_random_department(db, faculty.id)

    assert department
    assert isinstance(department, DepartmentResponse)
    assert department.id_faculte == faculty.id

    # Vérifier que la relation Faculty → Department existe
    statement = select(Department).where(Department.id == department.id)
    dep_db = db.execute(statement).scalar_one()
    assert dep_db is not None
    assert dep_db.id_faculte == faculty.id


def test_department_to_program_and_course_relation(db: Session) -> Any:
    faculty = create_random_faculty(db)
    department = create_random_department(db, faculty.id)
    program = create_random_program(db, department.id)
    course = create_random_course(db, program.id)

    # Vérifier les liens entre les 4 entités
    statement = select(Course).where(Course.id == course.id)
    course_db = db.execute(statement).scalar_one_or_none()
    assert course_db is not None
    assert course_db.id_parcours == program.id

    statement = select(Program).where(Program.id == program.id)
    prog_db = db.execute(statement).scalar_one_or_none()
    assert prog_db.id_departement == department.id

    statement = select(Department).where(Department.id == department.id)
    dep_db = db.execute(statement).scalar_one_or_none()
    assert dep_db.id_faculte == faculty.id


def test_update_department(db: Session) -> Any:
    faculty = create_random_faculty(db)
    department = create_random_department(db, faculty.id)
    update_data = DepartmentUpdate(nom="updated_department")

    updated = update_departement(db=db, dep_id=department.id, data=update_data)
    assert updated is not None
    assert updated.nom == "updated_department"


def test_delete_department(db: Session) -> Any:
    faculty = create_random_faculty(db)
    department = create_random_department(db, faculty.id)

    result = delete_department(db=db, department_id=department.id)
    assert result is True

    deleted = get_departement(db=db, department_id=department.id)
    assert deleted is None
