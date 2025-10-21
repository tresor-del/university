import uuid
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.university import Department
from app.tests.utils.university import create_random_faculty, create_random_department, create_random_departements
from app.core.settings import settings


def test_read_departments(client: TestClient, db: Session, superuser_token_headers: dict[str, str]):
    faculty = create_random_faculty(db)
    create_random_departements(db, faculty_id=faculty.id)

    response = client.get(
        f"{settings.API_V1_STR}/departments/?skip=0&limit=10",
        headers=superuser_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)
    assert data["count"] >= 3


def test_read_departments_without_auth(client: TestClient):
    response = client.get(f"{settings.API_V1_STR}/departments")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_department(client: TestClient, db: Session, superuser_token_headers: dict[str, str]):
    faculty = create_random_faculty(db)
    department_data = {
        "nom": "Département de Test",
        "description": "Description de test",
        "id_faculte": str(faculty.id)
    }

    response = client.post(
        f"{settings.API_V1_STR}/departments",
        json=department_data,
        headers=superuser_token_headers
    )
    assert response.status_code == 200
    department = response.json()
    assert department["nom"] == department_data["nom"]
    assert department["id"] is not None

def test_create_department_without_auth(client: TestClient, db: Session):
    faculty = create_random_faculty(db)
    department_data = {
        "nom": "Département de Test",
        "description": "Description de test",
        "id_faculte": str(faculty.id)
    }

    response = client.post(
        f"{settings.API_V1_STR}/departments",
        json=department_data
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_department_with_invalid_data(client: TestClient, db: Session, superuser_token_headers: dict[str, str]):
    department_data = {
        "description": "Description de test"
    }

    response = client.post(
        f"{settings.API_V1_STR}/departments",
        json=department_data,
        headers=superuser_token_headers
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY




def test_get_department(client: TestClient, db: Session, superuser_token_headers: dict[str, str]):
    faculty = create_random_faculty(db)
    department = create_random_department(db, faculty_id=faculty.id)

    response = client.get(
        f"{settings.API_V1_STR}/departments/{department.id}",
        headers=superuser_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(department.id)
    assert data["nom"] == department.nom


def test_get_department_not_found(client: TestClient, superuser_token_headers: dict[str, str]):
    response = client.get(
        f"{settings.API_V1_STR}/departments/{uuid.uuid4()}",
        headers=superuser_token_headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Departement non trouvé sur le système"


def test_update_department(client: TestClient, db: Session, superuser_token_headers: dict[str, str]):
    faculty = create_random_faculty(db)
    department = create_random_department(db, faculty_id=faculty.id)
    update_data = {"nom": "Nom mis à jour"}

    response = client.patch(
        f"{settings.API_V1_STR}/departments/{department.id}",
        json=update_data,
        headers=superuser_token_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nom"] == "Nom mis à jour"

    # Vérifier en base
    department_db = db.execute(select(Department).filter(Department.id == department.id)).scalar_one()
    assert department_db.nom == "Nom mis à jour"


def test_update_department_not_found(client: TestClient, superuser_token_headers: dict[str, str]):
    update_data = {"nom": "Nom mis à jour"}
    response = client.patch(
        f"{settings.API_V1_STR}/departments/{uuid.uuid4()}",
        json=update_data,
        headers=superuser_token_headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Departement non trouvé sur le système"
    
def test_update_department_with_invalid_data(client: TestClient, db: Session, superuser_token_headers: dict[str, str]):
    faculty = create_random_faculty(db)
    department = create_random_department(db, faculty_id=faculty.id)
    update_data = {"nom": None}

    response = client.patch(
        f"{settings.API_V1_STR}/departments/{department.id}",
        json=update_data,
        headers=superuser_token_headers
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT



def test_delete_department(client: TestClient, db: Session, superuser_token_headers: dict[str, str]):
    faculty = create_random_faculty(db)
    department = create_random_department(db, faculty_id=faculty.id)

    response = client.delete(
        f"{settings.API_V1_STR}/departments/{department.id}",
        headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Departement supprimé avec succès"

    # Vérifier en base
    department_db = db.execute(select(Department).filter(Department.id == department.id)).scalar_one_or_none()
    assert department_db is None


def test_delete_department_not_found(client: TestClient, superuser_token_headers: dict[str, str]):
    response = client.delete(
        f"{settings.API_V1_STR}/departments/{uuid.uuid4()}",
        headers=superuser_token_headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Departement non trouvé sur le système"