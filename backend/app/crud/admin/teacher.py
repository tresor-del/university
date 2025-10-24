from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.orm import Session


from app.models.teachers import Teacher
from app.schemas.teacher import TeachersResponse, TeacherResponse, TeacherCreate, TeacherUpdate

def teachers_list(*, db: Session, skip: int, limit: int) -> TeachersResponse | None:
    count_statement = select(func.count()).select_from(Teacher)
    count = db.execute(count_statement).scalar()
    
    statement = select(Teacher).offset(skip).limit(limit)
    data = db.execute(statement).scalars().all()
    return {"data": data, "count": count}

def create_teacher(db: Session, data: TeacherCreate)-> TeacherResponse | None:
    validate_data = data.model_dump()
    teacher = Teacher(**validate_data)
    db.add(teacher)
    db.commit()
    db.refresh(teacher)
    return TeacherResponse.model_validate(teacher)

def delete_teacher(*,db: Session, teacher_id: UUID) -> TeacherResponse | None:
    teacher = db.query(Teacher).filter(Teacher.id==teacher_id).first()
    if teacher:
        db.delete(teacher)
        db.commit()
        return True
    return False

def update_teacher(db: Session, teacher_id: UUID, data: TeacherUpdate) -> TeacherResponse | None:
    teacher = db.query(Teacher).filter(Teacher.id==teacher_id).first()
    if teacher:
        validate_data = data.model_dump(exclude_unset=True)
        for key, value in validate_data.items():
            setattr(teacher, key, value)
        db.commit()
        db.refresh(teacher)
        return TeacherResponse.model_validate(teacher)
    return None

def get_teacher(db: Session, id: UUID) -> TeacherResponse | None:
    statement = select(Teacher).where(Teacher.id==id)
    teacher = db.execute(statement).scalar_one_or_none()
    return TeacherResponse.model_validate(teacher) if teacher else None
