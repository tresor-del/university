import uvicorn
from typing import List

from fastapi import APIRouter, HTTPException, status

from app.schemas import schemas
from app.crud import students
from app.depends import SessionDeps
from app.routers.utils import handle_app_error


router =  APIRouter(prefix="/etudiants",tags=["Étudiants"])


@router.get("/", response_model=List[schemas.Etudiant])
async def get_students_list(db: SessionDeps):
    """
    Liste de tous les étudiants
    """
    try:
        return students.students_list(db)
    except Exception as e:
        handle_app_error(e)


@router.post("/enregistrer",)
async def enroll_student(data: schemas.EnrEtudiant, db: SessionDeps):
    """
    Enrégistrer un étudiant
    """
    try:
        return students.enroll_student(db, data)
    except Exception as e:
        handle_app_error(e)


@router.put("/modifier/{id}")
async def update_student(id: int, data: schemas.ModifierEtudiant, db: SessionDeps):
    """
    Modifier un etudiant
    """
    try:
        return students.update_student(db, id, data)
    except Exception as e:
        handle_app_error(e)


@router.delete("/effacer/{id}")
async def delete_student(id: int, db: SessionDeps):
    try: 
        return students.delete_student(db, id)
    except Exception as e:
        handle_app_error(e)

@router.get("/etudiant/{id}", response_model=schemas.Etudiant)
async def get_student(id: str, db: SessionDeps):
    try: 
        return students.get_student(db, id)
    except Exception as e:
        handle_app_error(e) 


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
