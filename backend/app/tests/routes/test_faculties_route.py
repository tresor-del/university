import uuid
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.university import Faculty
from app.tests.utils.university import create_random_faculty, create_random_faculties
from app.core.settings import settings


def test_read_faculties(client: TestClient, db: Session, superuser_token_headers: dict[str, str]):
    # Créer plusieurs facultés
    create_random_faculties(db)

    response = client.get(
        f"{settings.API_V1_STR}/faculties/?skip=0&limit=10",
        headers=superuser_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)
    assert data["count"] >= 3


def test_read_faculties_without_auth(client: TestClient):
    response = client.get(f"{settings.API_V1_STR}/faculties")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_faculty(client: TestClient, db: Session, superuser_token_headers: dict[str, str]):
    faculty_data = {
        "nom": "Faculté de Test",
        "description": "Description de test"
    }

    response = client.post(
        f"{settings.API_V1_STR}/faculties",
        json=faculty_data,
        headers=superuser_token_headers
    )
    assert response.status_code == 200
    faculty = response.json()
    assert faculty["nom"] == faculty_data["nom"]
    assert faculty["id"] is not None


def test_get_faculty(client: TestClient, db: Session, superuser_token_headers: dict[str, str]):
    faculty = create_random_faculty(db)

    response = client.get(
        f"{settings.API_V1_STR}/faculties/{faculty.id}",
        headers=superuser_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(faculty.id)
    assert data["nom"] == faculty.nom


def test_get_faculty_not_found(client: TestClient, superuser_token_headers: dict[str, str]):
    response = client.get(
        f"{settings.API_V1_STR}/faculties/{uuid.uuid4()}",
        headers=superuser_token_headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Faculté non trouvé sur le système"


def test_update_faculty(client: TestClient, db: Session, superuser_token_headers: dict[str, str]):
    faculty = create_random_faculty(db)
    update_data = {"nom": "Nom mis à jour"}

    response = client.patch(
        f"{settings.API_V1_STR}/faculties/{faculty.id}",
        json=update_data,
        headers=superuser_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nom"] == "Nom mis à jour"

    # Vérifier en base
    faculty_db = db.execute(select(Faculty).filter(Faculty.id == faculty.id)).scalar_one()
    assert faculty_db.nom == "Nom mis à jour"


def test_update_faculty_not_found(client: TestClient, superuser_token_headers: dict[str, str]):
    update_data = {"nom": "Nom mis à jour"}
    response = client.patch(
        f"{settings.API_V1_STR}/faculties/{uuid.uuid4()}",
        json=update_data,
        headers=superuser_token_headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Faculté non trouvé sur le système"


def test_delete_faculty(client: TestClient, db: Session, superuser_token_headers: dict[str, str]):
    faculty = create_random_faculty(db)

    response = client.delete(
        f"{settings.API_V1_STR}/faculties/{faculty.id}",
        headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Faculté supprimé avec succès"

    # Vérifier en base
    faculty_db = db.execute(select(Faculty).filter(Faculty.id == faculty.id)).scalar_one_or_none()
    assert faculty_db is None


def test_delete_faculty_not_found(client: TestClient, superuser_token_headers: dict[str, str]):
    response = client.delete(
        f"{settings.API_V1_STR}/faculties/{uuid.uuid4()}",
        headers=superuser_token_headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Faculté non trouvé sur le système"
