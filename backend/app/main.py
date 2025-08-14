import uvicorn
from fastapi import FastAPI

from database.db_utils import Database

from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder

from models import EnrEtudiant
from middlewares import setup_middleware


app = FastAPI()


setup_middleware(app)


def update_data(data):
    """
    Cette fonction prend un dictionnaire et le transforme en une requête sql
    """
    # prend tous les clés du dictionnaire et les joint avec des virgules
    columns = ','.join(data.keys())
    # parcourir les valeurs et entourer les chaînes avec '' mais laisser les les nombres
    values = ','.join(f"'{v}'" if isinstance(v, str) else str(v) for v in data.values())
    # construire la requête
    query = f"INSERT INTO AdzEtudiants ({columns}) VALUES ({values});"
    return query

@app.get("/etudiants")
def liste_etudiants():
    request = "SELECT * FROM AdzEtudiants"
    db = Database()
    result =  db.fetch_data(request)
    db.close()
    print(result)
    return result 

@app.post("/enregistrer_etudiant")
def enr_etudiant(data: EnrEtudiant):
    print(data)
    # transformer les données pydantic en un dictionnaire python
    updated_data = data.model_dump()
    print(updated_data)
    # utiliser les données pour faire une requête sql
    request = update_data(updated_data)
    # ouvir la base de donnée 
    db = Database()
    # faire la requête 
    result = db.insert_data(request)
    # fermer la base de donnée
    db.close()
    return {"message": "Etudiant enregistré", 'result': result}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
