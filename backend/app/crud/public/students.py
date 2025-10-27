from uuid import UUID
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.schemas.students import StudentPreInscription, StudentStatus
from app.models.students import Student

def pre_inscription_students(*, db: Session, data: StudentPreInscription):
    new_student = Student(
        **data.model_dump(),
        status = StudentStatus.BROUILLON
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    
    return new_student

def soumettre_pre_inscritpion(*, db: Session, student_id: UUID):
    student = db.get(Student, student_id)
    student.statut = StudentStatus.EN_ATTENTE
    student.date_soumission = func.now()
    db.commit()
    return True