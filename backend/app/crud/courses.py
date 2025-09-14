from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.schemas.university import (
    CourseCreate,
    CourseResponse,
    CoursesResponse,
    CourseUpdate
)
from app.models.university import Course



def read_courses(*, db: Session, skip: int, limit: int) -> CoursesResponse | None :
    count_statement = select(func.count()).select_from(Course)
    count = db.execute(count_statement).scalar()

    statement = select(Course).offset(skip).limit(limit)
    data = db.execute(statement).scalars().all()
    return CoursesResponse.model_validate({"data": data, "count": count})

def create_course(*, db: Session, data: CourseCreate) -> CourseResponse | None:
    validate_data = data.model_dump()
    course = Course(**validate_data)
    db.add(course)
    db.commit()
    db.refresh(course)
    return CourseResponse.model_validate(course)

def update_course(*, db: Session, course_id: UUID, data: CourseUpdate) -> CourseResponse | None:
    course = db.query(course).where(course.id==course_id).first()
    if course:
        validate_data = data.model_validate()
        for key, value in validate_data:
            setattr(course, key, value)
        db.commit()
        db.refresh(course)
        return CourseResponse.model_validate(course)
    return None

def delete_course(*, db: Session, course_id: UUID) -> CourseResponse | None:
    course = db.query(course).where(course.id==course_id).first()
    if course:
        db.delete(course)
        db.commit()
        return True
    return False


def get_course(*, db: Session, course_id: UUID) -> CourseResponse | None:
    statement = select(Course).where(Course.id==course_id)
    course = db.execute(statement).scalar_one()
    return course if course else None