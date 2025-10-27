from uuid import UUID

from sqlalchemy import func, select

from fastapi import APIRouter,  status
from fastapi.exceptions import HTTPException

from app.models.students import Student, StudentStatus
from app.schemas.message import Message
from app.crud.public.students import pre_inscription_students, soumettre_pre_inscritpion
from app.schemas.students import StudentPreInscription, StudentResponse
from app.api.deps import SessionDeps

router = APIRouter(prefix="/students/public/", tags=["Students"])


@router.post("/pre-inscription", status_code=status.HTTP_201_CREATED)
def pre_inscription_route(data: StudentPreInscription, db: SessionDeps) -> StudentResponse:
    """
    Permet à un étudiant de faire une pré-inscription en ligne (route publique)
    Le dossier sera en attente de validation par un admin
    """
    statement = select(Student).where(Student.email == data.email)
    existing_student = db.execute(statement).first()
    if existing_student:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Un dossier avec cet email existe déjà"
        )
    
    student = pre_inscription_students(db=db, data=data)
    return student


@router.post("/pre-inscription/{student_id}/soumettre")
def soumettre_pre_inscription(student_id: UUID, db: SessionDeps) -> Message:
    """
    Soumet le dossier de pré-inscription pour validation
    Change le statut de BROUILLON à EN_ATTENTE
    """
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dossier non trouvé"
        )
    
    if student.statut != StudentStatus.BROUILLON:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ce dossier ne peut pas être soumis (statut actuel: {student.statut})"
        )
    
    response = soumettre_pre_inscritpion(db=db, student_id=student_id)
    
    if response:
        return Message(message="Votre dossier a été soumis avec succès. Vous recevrez une notification une fois validé.")
