from app.tests.utils.students import random_user_data, create_random_student
from app.models.students import Etudiant

def test_liste_etudiants(client):
    response = client.get("/etudiants")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_enregistrer_etudiant(client):
    data = random_user_data()
    response = client.post("etudiants/enregistrer", json=data)
    assert response.status_code == 200
    
"""
Erreur pour les trois fonctions suivantes que je ne comprends pas
"""
def test_get_student(client, db):
    student = create_random_student(db)
    response = client.get(f"/etudiants/etudiant/{student.id}")
    assert response.status_code == 200    

def test_modifier_etudiant(client, db):
    student = create_random_student(db)
    data = random_user_data()
    response = client.put(f"/etudiants/modifier/{student.id}", json=data)
    assert response.status_code == 200

def test_effacer_etudiant(client, db):
    student = create_random_student(db)
    response = client.delete(f"/etudiants/effacer/{student.id}")
    assert response.status_code == 200