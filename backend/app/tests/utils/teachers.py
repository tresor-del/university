from sqlalchemy.orm import Session

from app.schemas.teacher import TeacherCreate, TeacherResponse
from app.crud.teacher import create_teacher
from app.tests.utils.utils import random_lower_string, random_phone, random_email

def create_random_teacher(db: Session) -> TeacherResponse:
    
    teacher_in = TeacherCreate(
        nom=random_lower_string(),
        prenom=random_lower_string(),
        email=random_email(),
        telephone=random_phone(),
        grade=random_lower_string()
    )
    return create_teacher(db=db, data=teacher_in)

def create_random_teachers(db: Session, count: int = 2) -> list[TeacherResponse]:
    teachers = []
    for _ in range(count): 
        teacher = create_random_teacher(db)
        teachers.append(teacher)
    return teachers

def random_teacher_data() -> TeacherCreate:
    teacher_in = TeacherCreate(
        nom=random_lower_string(),
        prenom=random_lower_string(),
        email=random_email(),
        telephone=random_phone(),
        grade=random_lower_string()
    )
    return teacher_in