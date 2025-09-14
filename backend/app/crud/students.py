from typing import Any
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.students import Student
from app.schemas.students import StudentResponse, StudentsResponse, StudentCreate, StudentUpdate


def students_list(*, db: Session, skip:int, limit: int) -> StudentsResponse | Any:
    count_statement = select(func.count()).select_from(Student)
    count = db.execute(count_statement).scalar()

    statement = select(Student).offset(skip).limit(limit)
    students = db.execute(statement).scalars().all()
    return StudentsResponse.model_validate({"data": students, "count": count})
    
def enroll_student(*, db: Session, data: StudentCreate) -> StudentResponse | Any:
    valid_data = data.model_dump()
    student = Student(**valid_data)
    db.add(student)
    db.commit()
    db.refresh(student)
    return StudentResponse.model_validate(student)   
        
def delete_student(*, db: Session, id: int) -> bool:
    student = db.query(Student).filter(Student.id == id).first()
    if student:
        db.delete(student)
        db.commit()
        return True
    return False

def update_student(*, db: Session, id: int, data: StudentUpdate) -> StudentResponse | Any:
    student = db.query(Student).filter(Student.id == id).first()
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(student, key, value)
    db.commit()
    db.refresh(student)
    return StudentResponse.model_validate(student) 

def get_student(*, db: Session, id: int) -> StudentResponse | Any:
    student = db.query(Student).filter(Student.id==id).first()
    return StudentResponse.model_validate(student) 