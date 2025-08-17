from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

def test_liste_etudiants():
    response = client.get("/etudiants")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_enregistrer_etudiant():
    data = {"id_etudiant": 999, "nom": "Test", "prenom": "User"}
    response = client.post("/enregistrer_etudiant", json=data)
    assert response.status_code == 200

def test_modifier_etudiant():
    data = {"nom": "Modif", "prenom": "User"}
    response = client.put("/modifier_etudiant/999", json=data)
    assert response.status_code == 200

def test_effacer_etudiant():
    response = client.delete("/effacer_etudiant/999")
    assert response.status_code == 200