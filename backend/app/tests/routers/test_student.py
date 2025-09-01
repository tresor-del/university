from fastapi import status


from app.core.settings import settings
from app.tests.utils.students import ( 
    random_user_data, 
    create_random_student, 
    create_random_students 
)


def test_liste_etudiants(client, db, superuser_token_headers: dict[str, str]):
    user = create_random_students(db)
    print(user)
    response = client.get(f"{settings.API_V1_STR}/etudiants/", headers=superuser_token_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# def test_enregistrer_etudiant(client):
#     student = random_user_data()
#     data =  student.model_dump()
#     if data.get("date_naissance"):
#         data["date_naissance"] = data["date_naissance"].isoformat()
#     response = client.post(f"{settings.API_V1_STR}/etudiants/enregistrer", json=data)
#     assert response.status_code == 200

# def test_get_student(client, db):
#     student = create_random_student(db)
#     print(student.id)
#     response = client.get(f"{settings.API_V1_STR}/etudiants/etudiant/{student.id}")
#     assert response.status_code == 200

# def test_modifier_etudiant(client, db):
#     student = create_random_student(db)
#     updated_data = random_user_data()
#     data = updated_data.model_dump(exclude_unset=True)
#     if data.get("date_naissance"):
#         data["date_naissance"] = data["date_naissance"].isoformat()
#     response = client.patch(f"{settings.API_V1_STR}/etudiants/modifier/{student.id}", json=data)
#     assert response.status_code == 200

# def test_effacer_etudiant(client, db):
    student = create_random_student(db)
    response = client.delete(f"{settings.API_V1_STR}/etudiants/effacer/{student.id}")
    assert response.status_code == 200