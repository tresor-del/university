import uuid
from uuid import UUID
from typing import Any
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud.courses import (
    read_courses,
    update_course,
    delete_course,
    get_course,
)
from app.models.university import Course
from app.schemas.university import CourseUpdate, CourseResponse
from app.tests.utils.university import  create_random_course, create_random_courses


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
