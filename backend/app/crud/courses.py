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

def create_course(*, db: Session, course_data: CourseCreate) -> CourseResponse | None:
    validate_data = course_data.model_dump()
    course = Course(**validate_data)
    db.add(course)
    db.commit()
    db.refresh(course)
    return CourseResponse.model_validate(course)

def update_course(*, db: Session, course_id: UUID, data: CourseUpdate) -> CourseResponse | None:
    course = db.get(Course, course_id)
    if course:
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(course, key, value)
        db.commit()
        db.refresh(course)
        return CourseResponse.model_validate(course)
    return None

def delete_course(*, db: Session, course_id: UUID) -> bool:
    course = db.get(Course, course_id)
    if course:
        db.delete(course)
        db.commit()
        return True
    return False

def get_course(*, db: Session, course_id: UUID) -> Course | None:
    statement = select(Course).where(Course.id==course_id)
    course = db.execute(statement).scalar_one_or_none()
    return course