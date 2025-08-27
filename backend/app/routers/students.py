import uvicorn
from typing import List

from fastapi import APIRouter, HTTPException, status

from app.schemas import schemas
from app.crud import students
from app.depends import SessionDeps
from app.routers.utils import handle_app_error


router =  APIRouter(prefix="/etudiants",tags=["Étudiants"])


@router.get("/", response_model=List[schemas.Etudiant])
async def liste_des_étudiants(db: SessionDeps):
    """
    Liste de tous les étudiants
    """
    try:
        return students.liste_etudiants(db)
    except Exception as e:
        handle_app_error(e)


@router.post("/enregistrer",)
async def enrégistrer_un_étudiant(data: schemas.EnrEtudiant, db: SessionDeps):
    """
    Enrégistrer un étudiant
    """
    try:
        return students.enr_etudiant(db, data)
    except Exception as e:
        handle_app_error(e)


@router.put("/modifier/{id}")
async def modifier_un_étudiant(id: int, data: schemas.ModifierEtudiant, db: SessionDeps):
    """
    Modifier un etudiant
    """
    try:
        return students.modifier_etudiant(db, id, data)
    except Exception as e:
        handle_app_error(e)


@router.delete("/effacer/{id}")
async def supprimer_un_étudiant(id: int, db: SessionDeps):
    return students.supprimer_etudiant(db, id)

@router.get("/etudiant/{id}", response_model=schemas.Etudiant)
async def recupérer_un_étudiant(id: str, db: SessionDeps):
    try: 
        return students.get_etudiant(db, id)
    except Exception as e:
        handle_app_error(e) 


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
