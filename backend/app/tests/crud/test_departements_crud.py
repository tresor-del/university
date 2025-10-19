from typing import Any
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud.departements import (
    update_departement,
    delete_department,
    get_departement,
)
from app.schemas.university import (
    DepartmentUpdate,
    DepartmentResponse,
)
from app.models.university import Department, Program, Course
from app.tests.utils.university import create_random_faculty, create_random_program, create_random_course, create_random_department


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
