from typing import Any, List
from uuid import UUID
import uuid
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud.admin.teacher import delete_teacher, get_teacher, update_teacher, teachers_list
from app.schemas.teacher import TeacherResponse, TeacherUpdate
from app.tests.utils.teachers import create_random_teacher, create_random_teachers
from app.tests.utils.utils import random_lower_string
from app.models.teachers import Teacher

def test_read_teachers(db: Session) -> Any:
    teachers = create_random_teachers(db)
    r = teachers_list(db=db, skip=1, limit=1)
    assert isinstance(r["data"], List)
    assert len(r["data"]) == 1
    assert r["count"] == len(teachers)
    
    for teacher in teachers:
        delete_teacher(db=db, teacher_id=teacher.id)

def test_create_teachers(db: Session) -> Any:
    teacher = create_random_teacher(db)
    assert teacher
    assert teacher.id_teacher is not None
    assert isinstance(teacher.id, UUID)
    assert isinstance(teacher, TeacherResponse)
    
    statement = select(Teacher).where(Teacher.id == teacher.id)
    teacher_db = db.execute(statement).scalar_one_or_none()
    assert teacher_db is not None
    assert teacher_db.id_teacher == teacher.id_teacher
    
    delete_teacher(db=db, teacher_id=teacher.id)

def test_delete_teacher(db: Session) -> Any:
    teacher = create_random_teacher(db)
    r = delete_teacher(db=db, teacher_id=teacher.id)
    assert r is True
    
    delete_teacher(db=db, teacher_id=teacher.id)
    
    statement = select(Teacher).where(Teacher.id == teacher.id)
    teacher_db = db.execute(statement).scalar_one_or_none()
    assert teacher_db is None
    
def test_delete_teacher_not_exists(db: Session) -> Any:
    r = delete_teacher(db=db, teacher_id=uuid.uuid4())
    assert r is False

def test_update_teacher(db: Session) -> Any:
    teacher = create_random_teacher(db)
    updated_name = random_lower_string()
    teacher_in = TeacherUpdate(nom=updated_name)
    r = update_teacher(db=db, teacher_id=teacher.id, data=teacher_in)
    assert r
    assert isinstance(r, TeacherResponse)
    assert r.nom == updated_name
    assert r.id_teacher == teacher.id_teacher
    
    statement = select(Teacher).where(Teacher.id == teacher.id)
    teacher_db = db.execute(statement).scalar_one_or_none()
    assert teacher_db is not None
    assert teacher_db.nom == updated_name
    
    delete_teacher(db=db, teacher_id=teacher.id)

def test_update_teacher_not_exists(db: Session) -> Any:
    updated_name = random_lower_string()
    teacher_in = TeacherUpdate(nom=updated_name)
    r = update_teacher(db=db, teacher_id=uuid.uuid4(), data=teacher_in)
    assert r is None

def test_get_teacher(db: Session) -> Any:
    teacher = create_random_teacher(db)
    r = get_teacher(db=db, id=teacher.id)
    assert isinstance(r, TeacherResponse)
    
    delete_teacher(db=db, teacher_id=teacher.id)

def test_get_teacher_not_exists(db: Session) -> Any:
    r = get_teacher(db=db, id=uuid.uuid4())
    assert r is None
