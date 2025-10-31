import uuid
from datetime import datetime
from typing import Any
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from fastapi import Body

from app.models.students import Student, StudentStatus
from app.schemas.students import StudentResponse, StudentsResponse, StudentCreate, StudentUpdate


def students_list(*, db: Session, skip:int, limit: int) -> StudentsResponse | Any:
    count_statement = select(func.count()).select_from(Student)
    count = db.execute(count_statement).scalar()

    statement = select(Student).offset(skip).limit(limit)
    students = db.execute(statement).scalars().all()
    return StudentsResponse.model_validate({"data": students, "count": count})

def get_pending_students(*, db: Session, skip: int = 0, limit: int) -> StudentsResponse | Any:
    count_statement = select(func.count()).select_from(Student).filter(Student.status == StudentStatus.EN_ATTENTE)
    count = db.execute(count_statement).scalar()
    
    statement = select(Student).where(Student.statut == StudentStatus.EN_ATTENTE).offset(skip).limit(limit)
    students = db.execute(statement).scalars().all()
    
    return StudentsResponse.model_validate({"data": students, "count": count})

def valider_student(*, db: Session, student_id: UUID) -> StudentsResponse | Any:
    student = db.get(Student, student_id)
    student.statut = StudentStatus.VALIDE
    student.date_validation = func.now()
    student.date_inscription = func.current_date()
    db.commit()
    db.refresh(student)
    return StudentResponse.model_validate(student)

def rejeter_student(*, db: Session, student_id: UUID, motif: str ) -> StudentResponse | Any:
    student  = db.get(Student, student_id)
    student.statut = StudentStatus.REJETTE
    student.motif_rejet = motif
    db.commit()
    return True
    
def enroll_student(*, db: Session, data: StudentCreate) -> StudentResponse | Any:
    student_data = data.model_dump()
    
    student_data['statut'] = StudentStatus.VALIDE
    student_data['date_inscription'] = func.current_date()
    student_data['date_validation'] = func.now()
    
    student = Student(**student_data)
    db.add(student)
    db.commit()
    db.refresh(student)
    return StudentResponse.model_validate(student)   
        
def delete_student(*, db: Session, id: UUID) -> bool:
    student = db.query(Student).filter(Student.id == id).first()
    if student:
        db.delete(student)
        db.commit()
        return True
    return False

def update_student(*, db: Session, id: UUID, data: StudentUpdate) -> StudentResponse | Any:
    student = db.query(Student).filter(Student.id == id).first()
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(student, key, value)
    db.commit()
    db.refresh(student)
    return StudentResponse.model_validate(student) 

def get_student(*, db: Session, id: UUID) -> StudentResponse | Any:
    student = db.query(Student).filter(Student.id==id).first()
    return StudentResponse.model_validate(student) 