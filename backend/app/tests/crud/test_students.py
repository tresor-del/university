from sqlalchemy.orm import Session

from app.schemas.schemas import EnrEtudiant
from app.models.students import Etudiant
from app.crud import students
from app.tests.utils.students import create_random_student, random_user_data, create_random_students
    
def test_create_student(db):
    student = create_random_student(db)
    assert student.id_etudiant is not None
    assert student.id is not None
    assert isinstance(student, Etudiant)
        
def test_delete_student(db):
    student = create_random_student(db)
    response = students.supprimer_etudiant(db, id=student.id)
    assert response["success"] == True

def test_modify_student(db):
    student = create_random_student(db)
    data = random_user_data()
    response = students.modifier_etudiant(db,id=student.id, data=data)
    assert response["success"] == True

def test_get_student(db):
    student = create_random_student(db)
    response = students.get_etudiant(db, student.id_etudiant)
    assert isinstance(response, Etudiant)

def test_list_student(db):
    create_random_students(db)
    response = students.liste_etudiants(db)
    assert isinstance(response, list)
    assert all(isinstance(item, Etudiant) for item in response)