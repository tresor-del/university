from typing import Any, List
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud.admin.faculty import (
    read_faculties,
    update_faculty,
    delete_faculty,
    get_faculty,
)
from app.schemas.university import  FacultyUpdate, FacultyResponse
from app.models.university import Faculty
from app.tests.utils.university import create_random_faculties, create_random_faculty


def test_read_faculties(db: Session) -> Any:
    faculties = create_random_faculties(db)
    r = read_faculties(db=db, skip=0, limit=1)

    assert isinstance(r.data, list)
    assert len(r.data) == 1
    assert r.count == len(faculties)

    for faculty in faculties:
        delete_faculty(db=db, faculty_id=faculty.id)


def test_create_faculty(db: Session) -> Any:
    faculty = create_random_faculty(db)
    assert faculty
    assert faculty.id is not None
    assert isinstance(faculty.id, UUID)
    assert isinstance(faculty, FacultyResponse)

    statement = select(Faculty).where(Faculty.id == faculty.id)
    faculty_db = db.execute(statement).scalar_one_or_none()
    assert faculty_db is not None
    assert faculty_db.nom == faculty.nom

    delete_faculty(db=db, faculty_id=faculty.id)


def test_update_faculty(db: Session) -> Any:
    faculty = create_random_faculty(db)
    update_data = FacultyUpdate(nom="updated_name")

    updated = update_faculty(db=db, faculty_id=faculty.id, data=update_data)
    assert updated is not None
    assert updated.nom == "updated_name"

    delete_faculty(db=db, faculty_id=faculty.id)


def test_delete_faculty(db: Session) -> Any:
    faculty = create_random_faculty(db)
    result = delete_faculty(db=db, faculty_id=faculty.id)
    assert result is True

    deleted = get_faculty(db=db, faculty_id=faculty.id)
    assert deleted is None
