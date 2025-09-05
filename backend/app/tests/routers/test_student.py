from fastapi import status

from app.crud import users
from app.schemas.users import UserCreate
from app.core.settings import settings
from app.tests.utils.students import ( 
    random_user_data,
    create_random_student, 
    create_random_students 
)


def test_liste_etudiants(
    client, 
    db, 
    superuser_token_headers: dict[str, str]
):
    create_random_students(db)
    response = client.get(
        f"{settings.API_V1_STR}/etudiants/", 
        headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_routes_etudiant_sans_auth(client):
    response = client.get(f"{settings.API_V1_STR}/etudiants/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_enregistrer_etudiant(
    client, 
    superuser_token_headers: dict[str, str]
):
    student = random_user_data()
    data =  student.model_dump()
    if data["date_naissance"]:
        data["date_naissance"] = data["date_naissance"].isoformat()
    response = client.post(
        f"{settings.API_V1_STR}/etudiants/enregistrer", 
        json=data,
        headers=superuser_token_headers
    )
    assert response.status_code == 200

def test_get_student(client, db, superuser_token_headers: dict[str, str]):
    student = create_random_student(db)
    print(student.id)
    response = client.get(
        f"{settings.API_V1_STR}/etudiants/etudiant/{student.id}",
        headers=superuser_token_headers
    )
    assert response.status_code == 200

def test_modifier_etudiant(client, db, superuser_token_headers: dict[str, str]):
    student = create_random_student(db)
    updated_data = random_user_data()
    data = updated_data.model_dump(exclude_unset=True)
    if data.get("date_naissance"):
        data["date_naissance"] = data["date_naissance"].isoformat()
    response = client.patch(
        f"{settings.API_V1_STR}/etudiants/modifier/{student.id}", 
        json=data,
        headers=superuser_token_headers
    )
    assert response.status_code == 200

def test_effacer_etudiant(client, db, superuser_token_headers: dict[str, str]):
    student = create_random_student(db)
    response = client.delete(
        f"{settings.API_V1_STR}/etudiants/effacer/{student.id}",
        headers=superuser_token_headers
    )
    assert response.status_code == 200