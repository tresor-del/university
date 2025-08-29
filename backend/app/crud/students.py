from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.exc import DatabaseError, DuplicateError, NotFoundError
from app.models import students
from app.schemas import schemas


def liste_etudiants(db: Session):
    etudiants = db.query(students.Etudiant).all()
    if etudiants:
        return etudiants
    raise DatabaseError("Erreur lors de la recupération de la liste des étudiants")

def enr_etudiant(db: Session, data: schemas.EnrEtudiant):
    try:
        etudiant = students.Etudiant(
        **data.model_dump()             
        )
        db.add(etudiant)
        db.commit()
        db.refresh(etudiant)
        return etudiant
    except IntegrityError:
        db.rollback()
        raise DuplicateError("Un étudiant avec ces informations existe déjà")
    except Exception:
        db.rollback()
        raise DatabaseError(
            "Erreur de la base de donnée lors de l'énrégistrement d'un étudiant"
        )
        
def supprimer_etudiant(db: Session, id: int):
    etudiant = db.query(students.Etudiant).filter(students.Etudiant.id == id).first()
    if etudiant:
        try:
            db.delete(etudiant)
            db.commit()
            return {f"success": True, "message": "Étudiant {id} supprimé avec succes"}
        except Exception:
            db.rollback()
            raise DatabaseError("Erreur inatendu lors de la suppression de l'étudiant")
    raise NotFoundError("Étudiant non trouvé")

def modifier_etudiant(db: Session, id: int, data: schemas.EnrEtudiant):
    etudiant = db.query(students.Etudiant).filter(students.Etudiant.id == id).first()
    if etudiant:
        try:
            etudiant.nom = data["nom"]
            etudiant.prenom = data["prenom"]
            etudiant.sexe = data["sexe"]
            db.commit()
            db.refresh(etudiant)
            return {"success": True,"message": f"Etudiant {id} modifié avec succes", "etudiant": etudiant}
        except Exception:
            raise DatabaseError("Erreur inatendu lors de la modification de l'étudiant")
    raise NotFoundError(f"Etudiant {id} non trouvé")

def get_etudiant(db: Session, id: int):
    etudiant = db.query(students.Etudiant).filter(students.Etudiant.id_etudiant==id).first()
    if etudiant:
        try:
            return etudiant
        except Exception:
            raise DatabaseError("Erreur inconnue")
    raise NotFoundError("L'étudiant {id} est introuvable")