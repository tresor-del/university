
def test_liste_etudiants(client):
    response = client.get("/etudiants")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_enregistrer_etudiant(client):
    data = {"nom": "Test", "prenom": "User", "sexe": "M"}
    response = client.post("/enregistrer_etudiant", json=data)
    assert response.status_code == 200

def test_modifier_etudiant(client):
    data = {"nom": "Modif", "prenom": "User", "sexe": "F"}
    response = client.put("/modifier_etudiant/999", json=data)
    assert response.status_code == 200

def test_effacer_etudiant(client):
    response = client.delete("/effacer_etudiant/999")
    assert response.status_code == 200