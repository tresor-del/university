from sqlalchemy.orm import Session

from app.models.students import Etudiant
from app.schemas.schemas import EnrEtudiant
from app.crud import students
from app.tests.utils.utils import random_lower_string, random_sexe


def create_random_student(db: Session) -> Etudiant:
    
    student_in = EnrEtudiant(
        nom=random_lower_string(), 
        prenom=random_lower_string(), 
        sexe=random_sexe()
    )
    student = students.enr_etudiant(db, student_in)
    return student


def create_random_students(db: Session) -> Etudiant:
    
    student_in_1 = EnrEtudiant(
        nom=random_lower_string(), 
        prenom=random_lower_string(), 
        sexe=random_sexe()
    )
    
    student_in_2 = EnrEtudiant(
        nom=random_lower_string(), 
        prenom=random_lower_string(), 
        sexe=random_sexe()
    )
    
    students.enr_etudiant(db, student_in_1)
    students.enr_etudiant(db, student_in_2)
    
    
    
def random_user_data():
    nom = random_lower_string()
    prenom = random_lower_string()
    sexe = random_sexe()
    return {"nom": nom, "prenom": prenom, "sexe": sexe}
    