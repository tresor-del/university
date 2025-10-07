from typing import Any, List
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud.courses import (
    read_courses,
    create_course,
    update_course,
    delete_course,
    get_course,
)
from app.models.university import Course, Program
from app.schemas.university import CourseCreate, CourseUpdate, CourseResponse, ProgramCreate
from app.tests.utils.utils import random_lower_string


def create_random_program(db: Session) -> Program:
    """Crée un programme aléatoire pour rattacher les cours."""
    data = ProgramCreate(
        nom=random_lower_string(),
        niveau="Licence",
        duree=3,
        id_departement=UUID(int=0), 
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


def test_read_courses(db: Session) -> Any:
    courses = create_random_courses(db)
    r = read_courses(db=db, skip=0, limit=1)

    assert isinstance(r["data"], list)
    assert len(r["data"]) == 1
    assert r["count"] == len(courses)

    for course in courses:
        delete_course(db=db, course_id=course.id)


def test_create_course(db: Session) -> Any:
    course = create_random_course(db)
    assert course
    assert course.id is not None
    assert isinstance(course.id, UUID)
    assert isinstance(course, CourseResponse)

    statement = select(Course).where(Course.id == course.id)
    course_db = db.execute(statement).scalar_one_or_none()
    assert course_db is not None
    assert course_db.titre == course.titre

    delete_course(db=db, course_id=course.id)


def test_update_course(db: Session) -> Any:
    course = create_random_course(db)
    update_data = CourseUpdate(titre="updated_title")

    updated = update_course(db=db, course_id=course.id, data=update_data)
    assert updated is not None
    assert updated.titre == "updated_title"

    delete_course(db=db, course_id=course.id)


def test_delete_course(db: Session) -> Any:
    course = create_random_course(db)
    result = delete_course(db=db, course_id=course.id)
    assert result is True

    deleted = get_course(db=db, course_id=course.id)
    assert deleted is None
