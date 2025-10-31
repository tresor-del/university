import uuid
from datetime import datetime
from typing import Any, List
from uuid import UUID

from sqlalchemy import select

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from app.api.deps import SessionDeps, get_current_active_admin
from app.models.students import Student, StudentStatus
from app.schemas.message import Message
from app.crud.admin.services_inscription.new_students import (
    students_list as crud_students_list,
    get_pending_students,
    valider_student,
    rejeter_student,
    enroll_student as crud_enroll_student,
    update_student as crud_update_student,
    delete_student as crud_delete_student,
    get_student as crud_get_student
)
from app.schemas.students import StudentResponse, StudentUpdate, StudentCreate, StudentsResponse

router = APIRouter(prefix="/students", tags=["Students"])


@router.get("/",dependencies=[Depends(get_current_active_admin)])
def get_students_list_route(db: SessionDeps, status: StudentStatus | None = None, skip: int = 1, limit: int = 100) -> StudentsResponse | Any:
    """
    Retourne une liste de tous les étudiants
    """
    return crud_students_list(db=db, skip=skip, limit=limit)

@router.get("/pending", dependancies=[Depends(get_current_active_admin)])
def get_pending_students_route(db: SessionDeps, skip: int = 0, limit: int = 100) -> StudentsResponse | Any:
    """
    Retourne la liste des dossiers en attente de validation
    """
    return get_pending_students(db=db, skip=skip, limit=limit)

@router.post("/{student_id}/valider", dependencies=[Depends(get_current_active_admin)])
def valider_student_route(db: SessionDeps, student_id: UUID) -> StudentResponse | Any:
    """
    Valide un dossier d'étudiant en attente
    Génère l'ID étudiant et change le statut à VALIDÉ
    """
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Étudiant non trouvé"
        )
    
    if student.statut != StudentStatus.EN_ATTENTE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ce dossier ne peut pas être validé (statut actuel: {student.statut})"
        )
    
    # Processus d'envoie d'Email, à faire plus tard
    
    student = valider_student(db=db, student_id=student_id)
    return student

@router.post("/{student_id}/rejeter", dependencies=[Depends(get_current_active_admin)])
def rejeter_student_route(db: SessionDeps, student_id: UUID, motif: str) -> StudentResponse | Any:
    """
    Rejette un étudiant avec un motif
    """
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Étudiant non trouvé"
        )
    
    if student.statut != StudentStatus.EN_ATTENTE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ce dossier ne peut pas être rejeté (statut actuel: {student.statut})"
        )
    
    response = rejeter_student(db=db, student_id=student_id, motif=motif)
    
    if response: 
        return Message(message="Étudiant rejeté avec succès")
    
      
@router.post("/", dependencies=[Depends(get_current_active_admin)])
def enroll_student_route(data: StudentCreate, db: SessionDeps) -> StudentResponse | Any:
    """
    Enrégistre un étudiant
    """
    statement = select(Student).where(Student.email==data.email)
    existing_student = db.execute(statement).first()
    if existing_student:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Il y a déjà un étudiant avec le même email"
        )
    return crud_enroll_student(db=db, data=data)

@router.get("/{student_id}", dependencies=[Depends(get_current_active_admin)])
def get_student_route(student_id: UUID, db: SessionDeps) -> StudentResponse | Any:
    """
    Retourne un étudiant présent dans la base de donnée
    """
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="L'étudiant recherché n'existe pas sur le systeme"
        )
    return crud_get_student(db=db, id=student_id)

@router.patch("/{student_id}", dependencies=[Depends(get_current_active_admin)])
def update_student_route(student_id: UUID, data: StudentUpdate, db: SessionDeps) -> StudentResponse | Any:
    """
    Modifie un étudiant
    """
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cet étudiant n'existe pas sur le systeme"
        )
    return crud_update_student(db=db, id=student_id, data=data)

@router.delete("/{student_id}", dependencies=[Depends(get_current_active_admin)])
def delete_student_route(student_id: UUID, db: SessionDeps) -> Message:
    """
    Supprime un étudiant du système
    """
    result = crud_delete_student(db=db, id=student_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cet étudiant n'existe pas sur le systeme"
        )
    return Message(message="Etudiant supprimé avec succès")

@router.post("/{student_id}/deactivate", dependencies=[Depends(get_current_active_admin)])
def deactivate_student(student_id: UUID, db: SessionDeps) -> Message:
    """
    Désactive un étudiant
    """
    student_db = db.query(Student).filter(Student.id==student_id).first()
    if not student_db:
        raise HTTPException(
            status_code=404,
            detail="Etudiant non trouvé sur le système"
        )
    student_db.statut = StudentStatus.DESACTIVE
    db.commit()
    db.refresh(student_db)
    return Message(message="Etudiant désactivé avec succès")

@router.post("/{student_id}/activate", dependencies=[Depends(get_current_active_admin)])
def activate_student(student_id: UUID, db: SessionDeps) -> Message:
    """
    Active un étudiant
    """
    student_db = db.query(Student).filter(Student.id==student_id).first()
    if not student_db:
        raise HTTPException(
            status_code=404,
            detail="Etudiant non trouvé sur le système"
        )
    student_db.statut = StudentStatus.ACTIF
    db.commit()
    db.refresh(student_db)
    return Message(message="Etudiant activé avec succès")

