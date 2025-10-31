from typing import Any
from app.schemas.students import StudentCreate, StudentResponse, StudentsResponse
from app.crud.admin.services_inscription import new_students
from app.tests.utils.students import (
    create_random_student, 
    random_user_data, 
    create_random_students
)
    
def test_create_student(db) -> Any:
    student = create_random_student(db)
    assert student.id_etudiant is not None
    assert student.id is not None
    assert isinstance(student, StudentResponse)
        
def test_delete_student(db) -> Any:
    student = create_random_student(db)
    response = new_students.delete_student(db=db, id=student.id)
    assert response is True

def test_update_student(db) -> Any:
    student = create_random_student(db)
    data = random_user_data()
    response = new_students.update_student(db=db,id=student.id, data=data)
    assert isinstance(response, StudentResponse)

def test_get_student(db) -> Any:
    student = create_random_student(db)
    response = new_students.get_student(db=db, id=student.id)
    assert isinstance(response, StudentResponse)

def test_list_student(db) -> Any:
    create_random_students(db)
    response = new_students.students_list(db=db, skip=1, limit=100)
    assert isinstance(response, StudentsResponse)