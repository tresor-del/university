from sqlalchemy.orm import Session

from sqlalchemy.orm import Session
from app.schemas.students import EnrollStudent
from app.models.students import Student
from app.crud.students import enroll_student
from app.tests.utils.utils import random_lower_string, random_sexe, random_email, random_date, random_phone

def create_random_student(db: Session) -> Student:
    """
    Créer un étudiant aléatoire et le retourner
    """
    student_in = EnrollStudent(
        nom=random_lower_string(),
        prenom=random_lower_string(),
        sexe=random_sexe(),
        date_naissance=random_date(2000, 2010),       
        lieu_naissance=random_lower_string(),
        nationalite=random_lower_string(),
        adresse=random_lower_string(),
        email=random_email(),
        telephone=random_phone(),
        nom_parent_tuteur=random_lower_string(),
        telephone_parent_tuteur=random_phone(),
        adresse_parent_tuteur=random_lower_string(),
        photo=None,
        statut="actif",
    )
    return enroll_student(db, student_in)


def create_random_students(db: Session, count: int = 2) -> list[Student]:
    """
    Créer plusieurs étudiants aléatoires
    """
    result = []
    for _ in range(count):
        student = create_random_student(db)
        result.append(student)
    return result


def random_user_data() -> EnrollStudent:
    """
    Retourne un schéma Pydantic complet avec données aléatoires
    """
    return EnrollStudent(
        nom=random_lower_string(),
        prenom=random_lower_string(),
        sexe=random_sexe(),
        date_naissance=random_date(2000, 2010),
        lieu_naissance=random_lower_string(),
        nationalite=random_lower_string(),
        adresse=random_lower_string(),
        email=random_email(),
        telephone=random_phone(),
        nom_parent_tuteur=random_lower_string(),
        telephone_parent_tuteur=random_phone(),
        adresse_parent_tuteur=random_lower_string(),
        photo=None,
        statut="actif",
    )

    