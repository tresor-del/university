from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.exc import DatabaseError, DuplicateError, NotFoundError
from app.models import students
from app.schemas import schemas


def students_list(db: Session):
    etudiants = db.query(students.Etudiant).all()
    if etudiants:
        return etudiants
    raise DatabaseError("Erreur lors de la recupération de la liste des étudiants")

def enroll_student(db: Session, data: schemas.EnrEtudiant):
    try:
        student = students.Etudiant(
        **data.model_dump()             
        )
        db.add(student)
        db.commit()
        db.refresh(student)
        return student
    except IntegrityError:
        db.rollback()
        raise DuplicateError("Un étudiant avec ces informations existe déjà")
    except Exception:
        db.rollback()
        raise DatabaseError(
            "Erreur de la base de donnée lors de l'énrégistrement d'un étudiant"
        )
        
def delete_student(db: Session, id: int):
    student = db.query(students.Etudiant).filter(students.Etudiant.id == id).first()
    if student:
        try:
            db.delete(student)
            db.commit()
            return {f"success": True, "message": "Étudiant {id} supprimé avec succes"}
        except Exception:
            db.rollback()
            raise DatabaseError("Erreur inatendu lors de la suppression de l'étudiant")
    raise NotFoundError("Étudiant non trouvé")

def update_student(db: Session, id: int, data: schemas.EnrEtudiant):
    student = db.query(students.Etudiant).filter(students.Etudiant.id == id).first()
    if student:
        try:
            student.nom = data["nom"]
            student.prenom = data["prenom"]
            student.sexe = data["sexe"]
            db.commit()
            db.refresh(student)
            return {"success": True,"message": f"Etudiant {id} modifié avec succes", "student": student}
        except Exception:
            raise DatabaseError("Erreur inatendu lors de la modification de l'étudiant")
    raise NotFoundError(f"Etudiant {id} non trouvé")

def get_student(db: Session, id: int):
    student = db.query(students.Etudiant).filter(students.Etudiant.id_etudiant==id).first()
    if student:
        try:
            return student
        except Exception:
            raise DatabaseError("Erreur inconnue")
    raise NotFoundError("L'étudiant {id} est introuvable")