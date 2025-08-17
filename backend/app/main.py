import uvicorn
from fastapi import FastAPI
from typing import List
from app.database.db_utils import Database

from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder

from app.models import EnrEtudiant, ModifierEtudiant, ListeEtudiant
from app.middlewares import setup_middleware


app = FastAPI()

# cors middleware
setup_middleware(app)

table = 'etudiants'

def save(data):
    columns = ','.join(data.keys())
    placeholders = ','.join(['%s'] * len(data))  
    query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders});"
    values = tuple(data.values())
    
    db = Database()
    result = db.execute(query, values)
    db.close()
    return result



@app.get("/etudiants")
def liste_etudiants():
    request =f"SELECT * FROM {table}"
    print(request)
    db = Database()
    result =  db.get_data(request)
    db.close()
    return result 

@app.post("/enregistrer_etudiant")
def enr_etudiant(data: EnrEtudiant):

    # transformer les données pydantic en un dictionnaire python
    updated_data = data.model_dump()
    print(updated_data)

    # utiliser les données pour faire une requête sql
    result = save(updated_data)
    return result

@app.put("/modifier_etudiant/{id}")
def modifier_etudiant(id: int, data: ModifierEtudiant):
    updated_data = data.model_dump()
    
    query = f"UPDATE {table} SET  nom=%s,prenom=%s WHERE id_etudiant=%s;"
    values = (updated_data['nom'], updated_data['prenom'], id)

    db = Database()
    result = db.execute(query, values)
    
    return result

@app.delete("/effacer_etudiant/{id}")
def effacer_etudiant(id: int):
    query = f"DELETE FROM {table} WHERE id_etudiant=%s;"
    value = (id,)

    db = Database()
    result = db.execute(query, value)

    return result

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
