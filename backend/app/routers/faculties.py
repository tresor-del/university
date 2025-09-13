from fastapi import Depends, dependencies
from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException

from app.deps import get_current_active_admin, SessionDeps
from app.models.university import Faculty
from app.schemas.message import Message
from app.schemas.university import FacultiesResponse, FacultyResponse, FacultyCreate, FacultyUpdate
from app.crud.faculty import (
    read_faculties,
    create_faculty,
    update_faculty,
    delete_faculty,
    get_faculty
)

router = APIRouter(prefix="/faculties", tags=["faculties"])



@router.get("/", dependencies=[Depends(get_current_active_admin)], response_model=FacultiesResponse)
def read_faculties_route(db: SessionDeps, skip: int = 0, limit: int = 100) -> FacultiesResponse:
    """
    Récupérer la liste de toutes les facultés
    """
    faculties = read_faculties(db=db, skip=skip, limit=limit)
    return faculties

@router.post("/", dependencies=[Depends(get_current_active_admin)], response_model=FacultyResponse)
def create_faculty_route(db: SessionDeps, data: FacultyCreate) -> FacultyResponse:
    """
    creéer une faculté
    """
    faculty = create_faculty(db=db, faculty_data=data)
    return faculty

@router.patch("/{faculty_id}", dependencies=[Depends(get_current_active_admin)], response_model=FacultyResponse)
def update_faculty_route(db: SessionDeps, faculty_id: int, data: FacultyUpdate) -> FacultyResponse:
    """
    Mets à jour une faculté
    """
    faculty = db.get(Faculty, faculty_id)
    if not faculty:
        raise HTTPException(
            status_code=404,
            detail="Faculté non trouvé sur le système"
        )
    faculty_updated = update_faculty(db=db, faculty_id=faculty_id, data=data)
    return faculty_updated

@router.delete("/{faculty_id}", dependencies=[Depends(get_current_active_admin)], response_model=Message)
def delete_faculty_route(db: SessionDeps, faculty_id: int) -> Message:
    """
    Supprime une faculté
    """
    result = delete_faculty(db=db, faculty_id=faculty_id)
    if result:
        return Message("Faculté supprimé avec succès")
    raise HTTPException(
            status_code=404,
            detail="Faculté non trouvé sur le système"
        )

@router.get("/{faculty_id}", dependencies=[Depends(get_current_active_admin)], response_model=FacultyResponse)
def get_faculty_route(db: SessionDeps, faculty_id: int) -> FacultyResponse:
    """
    Récupérer une faculté
    """
    faculty = get_faculty(db=db, faculty_id=faculty_id)
    if faculty:
        return faculty
    raise HTTPException(
        status_code=404,
        detail="Faculté non trouvé sur le système"
    )
