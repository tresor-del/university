from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.university import Faculty
from app.schemas.university import (
    FacultyBase,
    FacultyCreate,
    FacultyResponse,
    FacultiesResponse,
    FacultyUpdate,
)



def read_faculties(*, db: Session, skip: int, limit: int) -> FacultiesResponse | None:
    count_statement = select(func.count()).select_from(Faculty)
    count = db.execute(count_statement).scalar()

    statement = select(Faculty).offset(skip).limit(limit)
    data = db.execute(statement).scalars().all()
    return FacultiesResponse.model_validate({"data": data, "count": count})

def create_faculty(*, db: Session, faculty_data: FacultyCreate) -> FacultyResponse | None:
    validated_data = faculty_data.model_dump()
    faculty = Faculty(**validated_data)
    db.add(faculty)
    db.commit()
    db.refresh(faculty)
    return FacultyResponse.model_validate(faculty)

def update_faculty(*, db: Session, faculty_id: int, data: FacultyUpdate) -> FacultyResponse | None:
    faculty = db.query(Faculty).where(Faculty.id==faculty_id).first()
    if faculty:
        validate_data = data.model_validate()
        for key, value in validate_data:
            setattr(faculty, key, value)
        db.commit()
        db.refresh(faculty)
        return FacultyResponse.model_validate(faculty)
    return None

def delete_faculty(*, db: Session, faculty_id: int) -> FacultyResponse | None:
    faculty = db.query(Faculty).where(Faculty.id==faculty_id).first()
    if faculty:
        db.delete(faculty)
        db.commit()
        return True
    return False

def get_faculty(*, db: Session, faculty_id: int) -> FacultyResponse | None:
    statement = select(Faculty).where(Faculty.id==faculty_id)
    faculty = db.execute(statement).scalar_one()
    return faculty if faculty else None