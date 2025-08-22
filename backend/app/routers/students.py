import uvicorn
from app import schemas, crud
from app.crud import students

from typing import Annotated
from fastapi import APIRouter, Depends
from typing import List

from sqlalchemy.orm import Session

from app.middlewares import setup_middleware
from app.dependencies import get_db



app = router = APIRouter(
    prefix="/etudiants",
    tags=["étudiants"],
    dependencies=Annotated[Session, Depends(get_db)],
    responses={404: {"description": "Not found"}},
)


# cors middleware
setup_middleware(app)



# dependance
dependance_db = Annotated[Session, Depends(get_db)]

@app.get("/etudiants", response_model=List[schemas.Etudiant])
def liste_etudiants(db: dependance_db):
    
    liste = crud.liste_etudiants(db)
    print(liste)
    return liste

@app.post("/enregistrer_etudiant")
def enr_etudiant(data: schemas.EnrEtudiant, db: dependance_db):

    print(data)
    etudiant = crud.enr_etudiant(db, data)
    if etudiant:
        return {"success": True, "id": etudiant.id_etudiant}
    
    return {"success": False}


@app.put("/modifier_etudiant/{id}")
def modifier_etudiant(id: int, data: schemas.ModifierEtudiant, db: dependance_db):

    return crud.modifier_etudiant(db, id,data)


@app.delete("/effacer_etudiant/{id}")
def effacer_etudiant(id: int, db: dependance_db):

    return crud.supprimer_etudiant(db, id)

@app.get("/etudiant/{id}", response_model=schemas.Etudiant)
def recup_etudiant(id: str, db: dependance_db):
    return crud.get_etudiant(db, id)



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
