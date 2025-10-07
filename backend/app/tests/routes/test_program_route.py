import uuid
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.university import Program, Department, Faculty
from app.tests.utils.university import (
    create_random_faculty,
    create_random_department,
    create_random_program,
)
from app.core.settings import settings


# ------------------- LISTE -------------------
def test_list_programs(client: TestClient, db: Session, superuser_token_headers: dict[str, str]):
    faculty = create_random_faculty(db)
    department = create_random_department(db, faculty.id)
    for _ in range(3):
        create_random_program(db, department.id)

    response = client.get(
        f"{settings.API_V1_STR}/programs?skip=0&limit=10",
        headers=superuser_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)
    assert data["count"] >= 3


def test_list_programs_without_auth(client: TestClient):
    response = client.get(f"{settings.API_V1_STR}/programs")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# ------------------- CREATION -------------------
def test_create_program(client: TestClient, db: Session, superuser_token_headers: dict[str, str]):
    faculty = create_random_faculty(db)
    department = create_random_department(db, faculty.id)

    program_data = {
        "nom": "Programme Test",
        "niveau": "Licence",
        "duree": 3,
        "description": "Description test",
        "id_departement": str(department.id),
    }

    response = client.post(
        f"{settings.API_V1_STR}/programs",
        json=program_data,
        headers=superuser_token_headers
    )
    assert response.status_code == 200
    program = response.json()
    assert program["nom"] == "Programme Test"
    assert program["id_departement"] == str(department.id)


# ------------------- LECTURE -------------------
def test_get_program(client: TestClient, db: Session, superuser_token_headers: dict[str, str]):
    faculty = create_random_faculty(db)
    department = create_random_department(db, faculty.id)
    program = create_random_program(db, department.id)

    response = client.get(
        f"{settings.API_V1_STR}/programs/{program.id}",
        headers=superuser_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(program.id)
    assert data["nom"] == program.nom


def test_get_program_not_found(client: TestClient, superuser_token_headers: dict[str, str]):
    response = client.get(
        f"{settings.API_V1_STR}/programs/{uuid.uuid4()}",
        headers=superuser_token_headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Program non trouvé sur le système"


# ------------------- MISE A JOUR -------------------
def test_update_program(client: TestClient, db: Session, superuser_token_headers: dict[str, str]):
    faculty = create_random_faculty(db)
    department = create_random_department(db, faculty.id)
    program = create_random_program(db, department.id)

    update_data = {"nom": "Nom mis à jour"}
    response = client.patch(
        f"{settings.API_V1_STR}/programs/{program.id}",
        json=update_data,
        headers=superuser_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nom"] == "Nom mis à jour"

    # Vérifier en base
    program_db = db.execute(select(Program).filter(Program.id == program.id)).scalar_one()
    assert program_db.nom == "Nom mis à jour"


def test_update_program_not_found(client: TestClient, superuser_token_headers: dict[str, str]):
    update_data = {"nom": "Nom mis à jour"}
    response = client.patch(
        f"{settings.API_V1_STR}/programs/{uuid.uuid4()}",
        json=update_data,
        headers=superuser_token_headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Program non trouvé sur le système"


# ------------------- SUPPRESSION -------------------
def test_delete_program(client: TestClient, db: Session, superuser_token_headers: dict[str, str]):
    faculty = create_random_faculty(db)
    department = create_random_department(db, faculty.id)
    program = create_random_program(db, department.id)

    response = client.delete(
        f"{settings.API_V1_STR}/programs/{program.id}",
        headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Program supprimé avec succès"

    # Vérifier en base
    program_db = db.execute(select(Program).filter(Program.id == program.id)).scalar_one_or_none()
    assert program_db is None


def test_delete_program_not_found(client: TestClient, superuser_token_headers: dict[str, str]):
    response = client.delete(
        f"{settings.API_V1_STR}/programs/{uuid.uuid4()}",
        headers=superuser_token_headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Program non trouvé sur le système"
