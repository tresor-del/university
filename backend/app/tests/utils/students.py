from sqlalchemy.orm import Session

from app.models.students import Etudiant
from app.crud import students
from app.tests.utils.utils import random_lower_string, random_age, random_sexe

def create_random_student(db: Session) -> Etudiant:
    nom = random_lower_string()
    prenom = random_lower_string()
    age = random_age()
    sexe = random_sexe()
    student_in = Etudiant(nom=nom, prenom=prenom, age=age, sexe=sexe)
    student = students.enr_etudiant(db, student_in)
    return student
    