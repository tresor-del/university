from app.tests.utils.students import ( 
    random_user_data, 
    create_random_student, 
    create_random_students 
)


def test_liste_etudiants(client, db):
    user = create_random_students(db)
    print(user)
    response = client.get("/etudiants/")
    print(response)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_enregistrer_etudiant(client):
    student = random_user_data()
    data =  student.model_dump()
    if data.get("date_naissance"):
        data["date_naissance"] = data["date_naissance"].isoformat()
    response = client.post("/etudiants/enregistrer", json=data)
    assert response.status_code == 200

def test_get_student(client, db):
    student = create_random_student(db)
    print(student.id)
    response = client.get(f"/etudiants/etudiant/{student.id}")
    assert response.status_code == 200

def test_modifier_etudiant(client, db):
    student = create_random_student(db)
    updated_data = random_user_data()
    data = updated_data.model_dump(exclude_unset=True)
    if data.get("date_naissance"):
        data["date_naissance"] = data["date_naissance"].isoformat()
    response = client.patch(f"/etudiants/modifier/{student.id}", json=data)
    assert response.status_code == 200

def test_effacer_etudiant(client, db):
    student = create_random_student(db)
    response = client.delete(f"/etudiants/effacer/{student.id}")
    assert response.status_code == 200