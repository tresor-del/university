from typing import Any
from sqlalchemy.orm import Session
from uuid import uuid4

from app.crud.admin.programs import (
    create_program,
    read_programs,
    update_program,
    delete_program,
    get_program,
)
from app.schemas.university import ProgramCreate, ProgramUpdate, ProgramResponse
from app.models.university import Program, Course, Department, Faculty
from app.tests.utils.university import (
    create_random_faculty,
    create_random_department,
    create_random_program,
    create_random_course,
)



def test_create_program_with_department(db: Session) -> Any:
    faculty = create_random_faculty(db)
    department = create_random_department(db, faculty.id)
    program = create_random_program(db, department.id)

    assert program
    assert isinstance(program, Program)
    assert program.id_departement == department.id

    # Vérifier que le programme est bien en base
    program_db = get_program(db=db, program_id=program.id)
    assert program_db is not None
    assert program_db.id_departement == department.id


def test_program_to_course_relation(db: Session) -> Any:
    faculty = create_random_faculty(db)
    department = create_random_department(db, faculty.id)
    program = create_random_program(db, department.id)
    course = create_random_course(db, program.id)

    # Vérifier les liens Program → Course
    course_db = db.query(Course).filter(Course.id == course.id).first()
    assert course_db is not None
    assert course_db.id_parcours == program.id

    # Vérifier le lien Program → Department
    program_db = db.query(Program).filter(Program.id == program.id).first()
    assert program_db.id_departement == department.id

    # Vérifier le lien Department → Faculty
    department_db = db.query(Department).filter(Department.id == department.id).first()
    assert department_db.id_faculte == faculty.id


def test_read_programs(db: Session) -> Any:
    faculty = create_random_faculty(db)
    department = create_random_department(db, faculty.id)
    programs = [create_random_program(db, department.id) for _ in range(3)]

    result = read_programs(db=db, skip=0, limit=10)
    assert result["count"] >= 3
    assert all(isinstance(p, Program) for p in result["data"])


def test_update_program(db: Session) -> Any:
    faculty = create_random_faculty(db)
    department = create_random_department(db, faculty.id)
    program = create_random_program(db, department.id)

    update_data = ProgramUpdate(nom="updated_program")
    updated = update_program(db=db, program_id=program.id, data=update_data)

    assert updated is not None
    assert updated.nom == "updated_program"


def test_delete_program(db: Session) -> Any:
    faculty = create_random_faculty(db)
    department = create_random_department(db, faculty.id)
    program = create_random_program(db, department.id)

    result = delete_program(db=db, program_id=program.id)
    assert result is True

    deleted = get_program(db=db, program_id=program.id)
    assert deleted is None
