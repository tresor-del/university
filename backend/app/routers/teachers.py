from typing import Any, List

from sqlalchemy import func

from fastapi import Depends
from fastapi.routing import APIRouter

from app.deps import get_current_active_admin, SessionDeps, CurrentUser
from app.schemas import teacher as s_teacher
from app.schemas.message import Message
from app.crud import teacher



router = APIRouter(prefix="/teachers", tags="teachers")


@router.get("/",dependencies=Depends(get_current_active_admin), response_model=s_teacher.TeachersResponse)
def read_teachers_route(db: SessionDeps, skip: int = 0, limit: int = 100):
    """
    Retourne la liste de tous les proffesseurs
    """
    data = teacher.teachers_list(db=db, skip=skip, limit=limit)
    return s_teacher.TeachersResponse.model_validate(data)

@router.post("/create", response_model=s_teacher.TeacherResponse)
def create_teacher_route(db: SessionDeps,data: s_teacher.TeacherCreate, current_user=Depends(get_current_active_admin)):
    """
    Crée un nouveau proffesseur
    """
    return teacher.create_teacher(db=db, data=data)

@router.delete("/{teacher_id}", dependencies=Depends(get_current_active_admin))
def delete_teacher(db: SessionDeps, teacher_id: int) -> Message:
    result = teacher.delete_teacher(db=db, teacher_id=teacher_id)
    if result:
        return Message("Enseignant supprimé avec succès")
    
    