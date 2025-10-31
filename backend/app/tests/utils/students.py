from sqlalchemy.orm import Session

from sqlalchemy.orm import Session
from app.schemas.students import StudentCreate
from app.models.students import Student
from app.crud.admin.services_inscription.new_students import enroll_student
from app.tests.utils.utils import random_lower_string, random_sexe, random_email, random_date, random_phone

def create_random_student(db: Session) -> Student:
    """
    Créer un étudiant aléatoire et le retourner
    """
    student_in = StudentCreate(
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
        statut="actif",
        nom_du_pere = random_lower_string(),
        nom_de_la_mere = random_lower_string(),
        addresse_du_pere = random_lower_string(),
        addresse_de_la_mere = random_lower_string()
    )
    return enroll_student(db=db, data=student_in)


def create_random_students(db: Session, count: int = 2) -> list[Student]:
    """
    Créer plusieurs étudiants aléatoires
    """
    result = []
    for _ in range(count):
        student = create_random_student(db)
        result.append(student)
    return result


def random_user_data() -> StudentCreate:
    """
    Retourne un schéma Pydantic complet avec données aléatoires
    """
    return StudentCreate(
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
        statut="actif",
        nom_du_pere = random_lower_string(),
        nom_de_la_mere = random_lower_string(),
        addresse_du_pere = random_lower_string(),
        addresse_de_la_mere = random_lower_string()
    )

    