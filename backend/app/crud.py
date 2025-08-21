from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime


def liste_etudiants(db: Session):
    return db.query(models.Etudiant).all()

def enr_etudiant(db: Session, data: schemas.EnrEtudiant):
    db_etudiant = models.Etudiant(
        **data.model_dump()             
    )
    db.add(db_etudiant)
    db.commit()
    db.refresh(db_etudiant)
    return db_etudiant


def supprimer_etudiant(db: Session, id: int):
    etudiant = db.query(models.Etudiant).filter(models.Etudiant.id == id).first()
    if etudiant:
        db.delete(etudiant)
        db.commit()
        return True
    return False

def modifier_etudiant(db: Session, id: int, data: schemas.EnrEtudiant):
    etudiant = db.query(models.Etudiant).filter(models.Etudiant.id == id).first()
    if etudiant:
        etudiant.nom = data.nom
        etudiant.prenom = data.prenom
        etudiant.sexe = data.sexe
        
        db.commit()
        db.refresh(etudiant)
        return etudiant
    return None

def get_etudiant(db: Session, id: int):
    etudiant = db.query(models.Etudiant).filter(models.Etudiant.id_etudiant==id).first()
    if etudiant:
        return etudiant
    return False