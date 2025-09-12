from sqlalchemy import select, func
from sqlalchemy.orm import Session


from app.models.teachers import Teacher
from app.schemas.teacher import TeachersResponse, TeacherResponse, TeacherCreate, TeacherUpdate

def teachers_list(*, db: Session, skip: int, limit: int) -> TeacherResponse | None:
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
    return 

def delete_teacher(*,db: Session, teacher_id: int) -> TeacherResponse | None:
    teacher = db.query(Teacher).filter(Teacher.id==id).first()
    if teacher:
        db.delete(teacher)
        db.commit()
        return True
    return None

def update_teacher(db: Session, data: TeacherUpdate) -> TeacherResponse | None:
    teacher = db.query(Teacher).filter(Teacher.id==id).first()
    if teacher:
        validate_data = data.model_dump(exclude_unset=True)
        for key, value in validate_data:
            setattr(teacher, key, value)
        db.commit()
        db.refresh(teacher)
        return teacher
    return None

def get_teacher(db: Session, id: int) -> TeacherResponse | None:
    teacher = db.query(Teacher).filter(Teacher.id==id).first()
    return teacher if teacher else None
