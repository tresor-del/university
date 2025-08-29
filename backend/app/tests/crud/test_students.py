from sqlalchemy.orm import Session

from app.schemas.schemas import EnrollStudent
from app.models.students import Student
from app.crud import students
from app.tests.utils.students import create_random_student, random_user_data, create_random_students
    
def test_create_student(db):
    student = create_random_student(db)
    assert student.id_etudiant is not None
    assert student.id is not None
    assert isinstance(student, Student)
        
def test_delete_student(db):
    student = create_random_student(db)
    response = students.delete_student(db, id=student.id)
    assert response["success"] == True

def test_modify_student(db):
    student = create_random_student(db)
    data = random_user_data()
    response = students.update_student(db,id=student.id, data=data)
    assert response["success"] == True

def test_get_student(db):
    student = create_random_student(db)
    response = students.get_student(db, student.id_etudiant)
    assert isinstance(response, Student)

def test_list_student(db):
    create_random_students(db)
    response = students.students_list(db)
    assert isinstance(response, list)
    assert all(isinstance(item, Student) for item in response)