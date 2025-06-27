from typing import Any
import uuid
from fastapi import status

from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.students import Student
from app.tests.utils.students import ( 
    random_user_data,
    create_random_student, 
    create_random_students 
)
from app.core.settings import settings


# -------- LISTE --------
def test_liste_etudiants(client: TestClient, db: Session, superuser_token_headers: dict[str, str]):
    create_random_students(db)
    response = client.get(
        f"{settings.API_V1_STR}/students", 
        headers=superuser_token_headers
    )
    assert response.status_code == 200
    r = response.json()
    assert isinstance(r["data"], list)

def test_routes_etudiant_sans_auth(client):
    response = client.get(f"{settings.API_V1_STR}/students")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

# -------- CREATION --------
def test_enregistrer_etudiant(client: TestClient, db: Session, superuser_token_headers: dict[str, str]) -> Any:
    student = random_user_data()
    data = student.model_dump()
    if data.get("date_naissance"):
        data["date_naissance"] = data["date_naissance"].isoformat()

    response = client.post(
        f"{settings.API_V1_STR}/students", 
        json=data,
        headers=superuser_token_headers
    )
    assert response.status_code == 200 
    student = response.json()
    assert student["id"] is not None
    assert student["id_etudiant"] is not None

def test_creation_etudiant_avec_email_deja_existant(client:TestClient, db: Session, superuser_token_headers) -> Any:
    student = create_random_student(db)
    data = random_user_data().model_dump()
    data["email"] = student.email  
    if data.get("date_naissance"):
        data["date_naissance"] = data["date_naissance"].isoformat()

    response = client.post(
        f"{settings.API_V1_STR}/students",
        json=data,
        headers=superuser_token_headers
    )
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == "Il y a déjà un étudiant avec le même email"

def test_creation_etudiant_sans_champ_obligatoire(client: TestClient, superuser_token_headers) -> Any:
    data = {
        "nom": "tresor"
    }
    response = client.post(
        f"{settings.API_V1_STR}/students",
        json=data,
        headers=superuser_token_headers
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

# -------- LECTURE --------
def test_get_student(client: TestClient, db: Session, superuser_token_headers: dict[str, str]) -> Any:
    student = create_random_student(db)
    response = client.get(
        f"{settings.API_V1_STR}/students/{student.id}",
        headers=superuser_token_headers
    )
    assert response.status_code == 200 
    assert response.json()["id_etudiant"] == student.id_etudiant

def test_get_student_inexistant(client: TestClient, db: Session, superuser_token_headers: dict[str, str]) -> Any:
    response = client.get(
        f"{settings.API_V1_STR}/students/{uuid.uuid4()}",
        headers=superuser_token_headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "L'étudiant recherché n'existe pas sur le systeme"

# -------- MISE A JOUR --------
def test_modifier_etudiant(client: TestClient, db: Session, superuser_token_headers: dict[str, str]) -> Any:
    student = create_random_student(db)
    updated_data = {"nom": "updated_name"}
    response = client.patch(
        f"{settings.API_V1_STR}/students/{student.id}", 
        json=updated_data,
        headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert response.json()["id_etudiant"] == student.id_etudiant
    assert response.json()["nom"] == updated_data["nom"]
    
    student_query = select(Student).filter(Student.id==student.id)
    student = db.execute(student_query).scalar_one()
    assert student
    assert student.nom == updated_data["nom"]

def test_modifier_etudiant_inexistant(client: TestClient, db: Session, superuser_token_headers:  dict[str, str]) -> Any:
    student = create_random_student(db)
    updated_data = {"nom": "nouveau_nom"}
    response = client.patch(
        f"{settings.API_V1_STR}/students/{uuid.uuid4()}",
        json=updated_data,
        headers=superuser_token_headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Cet étudiant n'existe pas sur le systeme"

# -------- SUPPRESSION --------
def test_effacer_etudiant(client: TestClient, db: Session, superuser_token_headers: dict[str, str]) -> Any:
    student = create_random_student(db)
    response = client.delete(
        f"{settings.API_V1_STR}/students/{student.id}",
        headers=superuser_token_headers
    )
    assert response.status_code == 200

def test_effacer_etudiant_inexistant(client: TestClient,superuser_token_headers) -> Any:
    response = client.delete(
        f"{settings.API_V1_STR}/students/{uuid.uuid4()}",
        headers=superuser_token_headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

# -------- DESACTIVATION --------
def test_desactiver_etudiant(client: TestClient, superuser_token_headers: dict[str, str], db: Session):
    student = create_random_student(db)
    r = client.post(
        f"{settings.API_V1_STR}/students/{student.id}/deactivate",
        headers=superuser_token_headers
    )
    assert r.status_code == 200
    assert r.json()["message"] == "Etudiant désactivé avec succès"
    
    student_query = select(Student).filter(Student.id==student.id)
    student = db.execute(student_query).scalar_one()
    assert student
    assert student.statut == "désactivé"
    
def test_activer_etudiant(client: TestClient, superuser_token_headers: dict[str, str], db: Session):
    student = create_random_student(db)
    r = client.post(
        f"{settings.API_V1_STR}/students/{student.id}/activate",
        headers=superuser_token_headers
    )
    assert r.status_code == 200
    assert r.json()["message"] == "Etudiant activé avec succès"
    
    student_query = select(Student).filter(Student.id==student.id)
    student = db.execute(student_query).scalar_one()
    assert student
    assert student.statut == "actif"
    