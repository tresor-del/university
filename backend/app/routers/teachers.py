from typing import Any, List
from uuid import UUID

from sqlalchemy import func, select

from fastapi import Depends,status
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter

from app.deps import get_current_active_admin, SessionDeps
from app.schemas.teacher import TeacherUpdate, TeacherCreate, TeacherResponse, TeachersResponse
from app.schemas.message import Message
from app.models.teachers import Teacher
from app.crud import teacher



router = APIRouter(prefix="/teachers", tags=["teachers"])


@router.get("/",dependencies=[Depends(get_current_active_admin)])
def read_teachers_route(db: SessionDeps, skip: int = 0, limit: int = 100) -> TeachersResponse: 
    """
    Retourne la liste de tous les proffesseurs
    """
    data = teacher.teachers_list(db=db, skip=skip, limit=limit)
    return TeachersResponse.model_validate(data)

@router.post("/create", dependencies=[Depends(get_current_active_admin)])
def create_teacher_route(db: SessionDeps,data: TeacherCreate) -> TeacherResponse:
    """
    Crée un nouveau proffesseur
    """
    statement = select(Teacher).where(Teacher.email==data.email)
    existing_teacher = db.execute(statement).first()
    if existing_teacher:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Teacher with this email already exists"
        )
    return teacher.create_teacher(db=db, data=data)

@router.delete("/{teacher_id}", dependencies=[Depends(get_current_active_admin)])
def delete_teacher(db: SessionDeps, teacher_id: UUID) -> Message:
    result = teacher.delete_teacher(db=db, teacher_id=teacher_id)
    if result:
        return Message("Enseignant supprimé avec succès")
    raise  HTTPException(
        status_code=404,
        detail="Enseignant non trouvé"
    )
@router.patch("/{teacher_id}", dependencies=[Depends(get_current_active_admin)])
def update_teacher(db: SessionDeps, teacher_id: UUID, data: TeacherUpdate):
    db_teacher = db.get(Teacher, teacher_id)
    if not db_teacher:
        raise HTTPException(
            status_code=404,
            detail="Cet Enseignant n'est pas sur la base de donnée"
        )
    db_teacher = teacher.update_teacher(db=db, data=data, teacher_id=teacher_id)
    return db_teacher

@router.get("/{teacher_id}", response_model=TeacherResponse)
def get_teacher_route(db: SessionDeps, teacher_id: UUID):
    teacher_db = teacher.get_teacher(teacher_id)
    return teacher_db