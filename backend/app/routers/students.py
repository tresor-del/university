import uvicorn
from app.schemas import schemas
from app.crud import students

from typing import Annotated
from fastapi import APIRouter, Depends
from typing import List

from sqlalchemy.orm import Session

from app.dependencies import get_db



router =  APIRouter(
    prefix="/etudiants",
    tags=["Étudiants"],
    # dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)


# dependance
dependance_db = Annotated[Session, Depends(get_db)]


@router.get(
    "/", 
    response_model=List[schemas.Etudiant],
)
async def liste_des_étudiants(db: dependance_db):
    liste = students.liste_etudiants(db)
    print(liste)
    return liste


@router.post(
    "/enregistrer",
)
async def enrégistrer_un_étudiant(data: schemas.EnrEtudiant, db: dependance_db):

    print(data)
    etudiant = students.enr_etudiant(db, data)
    if etudiant:
        return {"success": True, "id": etudiant.id_etudiant}
    return {"success": False}


@router.put(
    "/modifier/{id}",  
)
async def modifier_un_étudiant(id: int, data: schemas.ModifierEtudiant, db: dependance_db):
    return students.modifier_etudiant(db, id,data)


@router.delete(
    "/effacer/{id}",
)
async def supprimer_un_étudiant(id: int, db: dependance_db):
    return students.supprimer_etudiant(db, id)

@router.get(
    "/etudiant/{id}",
    response_model=schemas.Etudiant
)
async def recupérer_un_étudiant(id: str, db: dependance_db):
    return students.get_etudiant(db, id)



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
