import uvicorn

from . import schemas, crud

from fastapi import FastAPI, Depends
from typing import List
from .database.config import sessionLocal, engine, Base

from sqlalchemy.orm import Session

from .middlewares import setup_middleware

# Créer toutes les tables dans la base qui sont décrites par les classes héritant de Base
Base.metadata.create_all(bind=engine)

app = FastAPI()

# cors middleware
setup_middleware(app)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/etudiants", response_model=List[schemas.EnrEtudiant])
def liste_etudiants(db: Session = Depends(get_db)):
    
    liste = crud.liste_etudiants(db)
    print(liste)
    return liste

@app.post("/enregistrer_etudiant")
def enr_etudiant(data: schemas.EnrEtudiant, db: Session = Depends(get_db)):

    print(data)
    etudiant = crud.enr_etudiant(db, data)
    if etudiant:
        return {"success": True}
    return {"success": False}


@app.put("/modifier_etudiant/{id}")
def modifier_etudiant(id: int, data: schemas.ModifierEtudiant, db: Session = Depends(get_db)):

    return crud.modifier_etudiant(db, id,data)


@app.delete("/effacer_etudiant/{id}")
def effacer_etudiant(id: int, db: Session = Depends(get_db)):

    return crud.supprimer_etudiant(db, id)



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
