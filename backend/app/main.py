import uvicorn
from fastapi import FastAPI

from database.db_utils import Database

from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder

from models import EnrEtudiant


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def update_data(data):
    columns = ','.join(data.keys())
    values = ','.join(f"'{v}'" if isinstance(v, str) else str(v) for v in data.values())
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
    updated_data = data.model_dump()
    print(updated_data)
    request = update_data(updated_data)
    db = Database()
    result = db.fetch_data(request)
    db.close()
    return {"message": "Etudiant enregistré", 'result': result}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
