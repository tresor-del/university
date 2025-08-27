from sqlalchemy.orm import Session

from app.models.students import Etudiant
from app.crud import students
from app.tests.utils.utils import random_lower_string, random_age, random_sexe

    
def test_create_student(db_etudiant):
    nom = random_lower_string()
    prenom = random_lower_string()
    age = random_age()
    sexe = random_sexe()
    student_in = Etudiant(nom=nom, prenom=prenom, age=age, sexe=sexe)
    student = students.enr_etudiant(db_etudiant, student_in)
    assert student.id_etudiant is not None
    assert isinstance(student, Etudiant)
        
