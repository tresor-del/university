from fastapi import APIRouter, Depends
from typing import List
from app.deps import SessionDeps, get_current_active_admin
from app.routers.utils import handle_app_error
from app.crud.students import (
    students_list as crud_students_list,
    enroll_student as crud_enroll_student,
    update_student as crud_update_student,
    delete_student as crud_delete_student,
    get_student as crud_get_student
)
from app.schemas.students import (
    StudentModel,
    EnrollStudent, 
    UpdateStudent, 
    PublicStudent
)

router = APIRouter(prefix="/etudiants", tags=["Étudiants"])


@router.get("/", response_model=List[StudentModel])
def get_students_list_route(
    db: SessionDeps,
    current_user=Depends(get_current_active_admin)
):
    """
    Retourne une liste de tous les étudiants
    """
    try:
        return crud_students_list(db)
    # pour le test (à remplacer)
    except Exception as e:
        import traceback
        print("Erreur dans get_students_list_route:", e)
        traceback.print_exc()
        raise

@router.post("/enregistrer")
def enroll_student_route(
    data: EnrollStudent, 
    db: SessionDeps,
    current_user=Depends(get_current_active_admin)
):
    """
    Enrégistre un étudiant
    """
    try:
        return crud_enroll_student(db, data)
    except Exception as e:
        handle_app_error(e)

@router.get("/etudiant/{id}", response_model=PublicStudent)
def get_student_route(
    id: int, 
    db: SessionDeps,
    current_user=Depends(get_current_active_admin)
):
    """
    Retourne un étudiant dans la base de donnée
    """
    try:
        return crud_get_student(db, id)
    except Exception as e:
        handle_app_error(e)

@router.patch("/modifier/{id}")
def update_student_route(
    id: int, 
    data: UpdateStudent, 
    db: SessionDeps,
    current_user=Depends(get_current_active_admin)
):
    """
    Modifie un étudiant
    """
    try:
        return crud_update_student(db, id, data)
    except Exception as e:
        handle_app_error(e)

@router.delete("/effacer/{id}")
def delete_student_route(
    id: int, 
    db: SessionDeps,
    current_user=Depends(get_current_active_admin)
):
    """
    Modifie un étudiant
    """
    try:
        return crud_delete_student(db, id)
    except Exception as e:
        handle_app_error(e)
