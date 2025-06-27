import uuid

from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi.testclient import TestClient

from app.schemas.teacher import TeacherCreate, TeacherResponse
from app.crud.teacher import delete_teacher
from app.core.config import settings
from app.tests.utils.teachers import create_random_teachers, random_teacher_data, create_random_teacher
from app.tests.utils.utils import random_email, random_lower_string, random_phone
from app.models.teachers import Teacher

# -------- LISTE --------
def test_read_teachers_route_default(db: Session, client: TestClient, superuser_token_headers: dict[str, str]) -> Any:
    teachers = create_random_teachers(db)
    r = client.get(
        f"{settings.API_V1_STR}/teachers",
        headers=superuser_token_headers
    )
    assert r.status_code == 200
    response = r.json()
    assert response["count"] == 2
    assert [isinstance(item, TeacherResponse) for item in response["data"]]
    
    # supprimer les teachers crées dans la base de donnée
    for teacher in teachers:
        delete_teacher(db=db, teacher_id=teacher.id)
    
def test_read_teachers_route_query(db: Session, client: TestClient, superuser_token_headers: dict[str, str]) ->Any:
    teachers = create_random_teachers(db)
    teachers2 = create_random_teachers(db)
    r = client.get(
        f"{settings.API_V1_STR}/teachers/?limit=3",
        headers=superuser_token_headers
    )
    assert r.status_code == 200
    
    response = r.json()
    assert response["count"] == 4
    assert len(response["data"]) == 3
    assert [isinstance(item, TeacherResponse) for item in response["data"]]
    
    for teacher in teachers:
        delete_teacher(db=db, teacher_id=teacher.id)
        
    for teacher in teachers2:
        delete_teacher(db=db, teacher_id=teacher.id)

# -------- CREATION --------
def test_create_teacher(db: Session, client: TestClient, superuser_token_headers: dict[str, str]) -> Any:
    teacher_in = random_teacher_data()
    r = client.post(
        f"{settings.API_V1_STR}/teachers/create",
        headers=superuser_token_headers,
        json=teacher_in.model_dump()
    )
    assert r.status_code == 200
    response = r.json()
    assert response["id_teacher"]
    

def test_create_teacher_email_exists_error(db: Session, client: TestClient, superuser_token_headers: dict[str, str]) -> Any:
    teacher = create_random_teacher(db)
    teacher_in = TeacherCreate(
        nom=random_lower_string(),
        prenom=random_lower_string(),
        email=teacher.email,
        telephone=random_phone(),
        grade=random_lower_string()
    )
    r = client.post(
        f"{settings.API_V1_STR}/teachers/create",
        headers=superuser_token_headers,
        json=teacher_in.model_dump()
    )
    assert r.status_code == 409
    assert r.json()["detail"] == "Teacher with this email already exists"
    
def test_create_teacher_invalid_data(db: Session, client: TestClient, superuser_token_headers: dict[str, str]) -> Any:
    data = {"nom": "random_name"}
    r = client.post(
        f"{settings.API_V1_STR}/teachers/create",
        json=data,
        headers=superuser_token_headers
    )
    assert r.status_code == 422

# -------- SUPPRESSION --------
def test_delete_teacher_route(db: Session, client: TestClient, superuser_token_headers: dict[str, str]) -> Any:
    teacher = create_random_teacher(db)
    r = client.delete(
        f"{settings.API_V1_STR}/teachers/{teacher.id}",
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    response = r.json()
    assert response["message"] == "Teacher deleted successfully"
    
    delete_teacher(db=db, teacher_id=teacher.id)

def test_delete_teacher_not_exists(db: Session, client: TestClient, superuser_token_headers: dict[str, str]) -> Any:
    teacher = create_random_teacher(db)
    r = client.delete(
        f"{settings.API_V1_STR}/teachers/{uuid.uuid4()}",
        headers=superuser_token_headers
    )
    assert r.status_code == 404
    response = r.json()
    assert response["detail"] == "Teacher not found"

# -------- MISE A JOUR --------
def test_update_teacher_route(db: Session, client: TestClient, superuser_token_headers: dict[str, str]) -> Any:
    teacher = create_random_teacher(db)
    update_data = {"nom": "updated_name"}
    r = client.patch(
        f"{settings.API_V1_STR}/teachers/{teacher.id}",
        json=update_data, 
        headers=superuser_token_headers
    )
    assert r.status_code == 200
    response = r.json()
    assert response["nom"] == "updated_name"

    statement = select(Teacher).where(Teacher.id==teacher.id)
    db_teacher = db.execute(statement).scalar_one_or_none()
    assert db_teacher
    assert db_teacher.nom == "updated_name"
    
    delete_teacher(db=db, teacher_id=teacher.id)

def test_update_teacher_not_exists_error(db: Session, client: TestClient, superuser_token_headers: dict[str, str]) -> Any:
    update_data = {"nom": "updated_name"}
    r = client.patch(
        f"{settings.API_V1_STR}/teachers/{uuid.uuid4()}",
        json=update_data, 
        headers=superuser_token_headers,
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "Teacher not found"

# -------- RÉCUPÉRATION --------
def test_get_teacher_route(db: Session, client: TestClient, superuser_token_headers: dict[str, str]) -> Any:
    teacher = create_random_teacher(db)
    r = client.get(
        f"{settings.API_V1_STR}/teachers/{teacher.id}",
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    response = r.json()
    assert response["id_teacher"] is not None
    
    delete_teacher(db=db, teacher_id=teacher.id)

def test_get_teacher_not_exist_error(db: Session, client: TestClient, superuser_token_headers: dict[str, str]) -> Any:
    r = client.get(
        f"{settings.API_V1_STR}/teachers/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert r.status_code == 404
    response = r.json()
    assert response["detail"] == "Teacher not found"