from typing import Any

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.tests.utils.university import (
    create_random_faculty,
    create_random_departements
)


def test_read_departements(db: Session, client: TestClient) -> None:
    faculty = create_random_faculty(db=db)
    create_random_departements(db=db, faculty_id=faculty.id)
    