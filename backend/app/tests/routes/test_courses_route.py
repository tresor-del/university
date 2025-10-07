import uuid
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.university import Course
from app.tests.utils.university import (
    create_random_faculty,
    create_random_department,
    create_random_program,
    create_random_course,
)
from app.core.settings import settings


# ------------------- LISTE -------------------
def test_list_courses(client: TestClient, db: Session, superuser_token_headers: dict[str, str]):
    faculty = create_random_faculty(db)
    department = create_random_department(db, faculty.id)
    program = create_random_program(db, department.id)
    for _ in range(3):
        create_random_course(db, program.id)

    response = client.get(
        f"{settings.API_V1_STR}/courses?skip=0&limit=10",
        headers=superuser_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)
    assert data["count"] >= 3


def test_list_courses_without_auth(client: TestClient):
    response = client.get(f"{settings.API_V1_STR}/courses")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# ------------------- CREATION -------------------
def test_create_course(client: TestClient, db: Session, superuser_token_headers: dict[str, str]):
    faculty = create_random_faculty(db)
    department = create_random_department(db, faculty.id)
    program = create_random_program(db, department.id)

    course_data = {
        "code": "CS101",
        "titre": "Intro CS",
        "description": "Test course",
        "credits": 4,
        "id_parcours": str(program.id),
    }

    response = client.post(
        f"{settings.API_V1_STR}/courses",
        json=course_data,
        headers=superuser_token_headers
    )
    assert response.status_code == 200
    course = response.json()
    assert course["id_parcours"] == str(program.id)
    assert course["code"] == "CS101"


# ------------------- LECTURE -------------------
def test_get_course(client: TestClient, db: Session, superuser_token_headers: dict[str, str]):
    faculty = create_random_faculty(db)
    department = create_random_department(db, faculty.id)
    program = create_random_program(db, department.id)
    course = create_random_course(db, program.id)

    response = client.get(
        f"{settings.API_V1_STR}/courses/{course.id}",
        headers=superuser_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(course.id)


def test_get_course_not_found(client: TestClient, superuser_token_headers: dict[str, str]):
    response = client.get(
        f"{settings.API_V1_STR}/courses/{uuid.uuid4()}",
        headers=superuser_token_headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Cours non trouvé sur le système"


# ------------------- MISE A JOUR -------------------
def test_update_course(client: TestClient, db: Session, superuser_token_headers: dict[str, str]):
    faculty = create_random_faculty(db)
    department = create_random_department(db, faculty.id)
    program = create_random_program(db, department.id)
    course = create_random_course(db, program.id)

    update_data = {"titre": "Updated Title"}
    response = client.patch(
        f"{settings.API_V1_STR}/courses/{course.id}",
        json=update_data,
        headers=superuser_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["titre"] == "Updated Title"

    # Vérifier en base
    course_db = db.execute(select(Course).filter(Course.id == course.id)).scalar_one()
    assert course_db.titre == "Updated Title"


def test_update_course_not_found(client: TestClient, superuser_token_headers: dict[str, str]):
    update_data = {"titre": "Updated Title"}
    response = client.patch(
        f"{settings.API_V1_STR}/courses/{uuid.uuid4()}",
        json=update_data,
        headers=superuser_token_headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Cours non trouvé sur le système"


# ------------------- SUPPRESSION -------------------
def test_delete_course(client: TestClient, db: Session, superuser_token_headers: dict[str, str]):
    faculty = create_random_faculty(db)
    department = create_random_department(db, faculty.id)
    program = create_random_program(db, department.id)
    course = create_random_course(db, program.id)

    response = client.delete(
        f"{settings.API_V1_STR}/courses/{course.id}",
        headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Cours supprimé avec succès"

    # Vérifier que le cours n’existe plus
    course_db = db.execute(select(Course).filter(Course.id == course.id)).scalar_one_or_none()
    assert course_db is None


def test_delete_course_not_found(client: TestClient, superuser_token_headers: dict[str, str]):
    response = client.delete(
        f"{settings.API_V1_STR}/courses/{uuid.uuid4()}",
        headers=superuser_token_headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Cours non trouvé sur le système"
