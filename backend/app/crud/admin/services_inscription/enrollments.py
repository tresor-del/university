# app/crud/admin/services_inscription/enrollments.py
from typing import Optional, List
from uuid import UUID
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.students import Student, StudentStatus
from app.models.enrollments import Enrollment
from app.models.student_history import StudentHistory


# ============ INSCRIPTION NOUVELLE ANNÉE ============

def create_enrollment(
    *,
    db: Session,
    student_id: UUID,
    annee_academique: str,
    niveau: str,
    id_departement: int,
    id_parcours: int
) -> Enrollment:
    """
    Crée une nouvelle inscription pour une année académique
    """
    new_enrollment = Enrollment(
        student_id=student_id,
        annee_academique=annee_academique,
        niveau=niveau,
        id_departement=id_departement,
        id_parcours=id_parcours,
        date_inscription=func.current_date(),
        statut="en_cours"
    )
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)
    return new_enrollment


def get_enrollment_by_student_and_year(
    db: Session,
    student_id: UUID,
    annee_academique: str
) -> Optional[Enrollment]:
    """
    Récupère l'inscription d'un étudiant pour une année donnée
    """
    return db.query(Enrollment).filter(
        Enrollment.student_id == student_id,
        Enrollment.annee_academique == annee_academique
    ).first()


def update_student_academic_info(
    db: Session,
    student_id: UUID,
    id_parcours: Optional[int] = None,
    id_departement: Optional[int] = None
) -> Student:
    """
    Met à jour les informations académiques d'un étudiant
    """
    student = db.get(Student, student_id)
    if not student:
        return None
    
    if id_parcours:
        student.id_parcours = id_parcours
    if id_departement:
        student.id_departement = id_departement
    
    db.commit()
    db.refresh(student)
    return student


# ============ CLÔTURE ANNÉE ACADÉMIQUE ============

def close_enrollment(
    *,
    db: Session,
    enrollment_id: int,
    est_admis: bool,
    moyenne_annuelle: Optional[float] = None,
    credits_obtenus: int = 0
) -> Enrollment:
    """
    Clôture une inscription (fin d'année académique)
    """
    enrollment = db.get(Enrollment, enrollment_id)
    if not enrollment:
        return None
    
    enrollment.statut = "validée" if est_admis else "échouée"
    enrollment.est_admis = est_admis
    enrollment.moyenne_annuelle = moyenne_annuelle
    enrollment.credits_obtenus = credits_obtenus
    
    db.commit()
    db.refresh(enrollment)
    return enrollment


# ============ DIPLÔMER UN ÉTUDIANT ============

def get_last_enrollment(db: Session, student_id: UUID) -> Optional[Enrollment]:
    """
    Récupère la dernière inscription d'un étudiant
    """
    return db.query(Enrollment).filter(
        Enrollment.student_id == student_id
    ).order_by(Enrollment.date_inscription.desc()).first()


def mark_student_as_graduated(
    db: Session,
    student_id: UUID,
    type_diplome: str,
    mention: Optional[str] = None
) -> Student:
    """
    Marque un étudiant comme diplômé (ancien)
    """
    student = db.get(Student, student_id)
    if not student:
        return None
    
    # Récupérer la dernière inscription
    last_enrollment = get_last_enrollment(db, student_id)
    
    if last_enrollment:
        last_enrollment.statut = "validée"
        last_enrollment.est_admis = True
    
    # Marquer comme ancien
    student.statut = StudentStatus.ANCIEN
    student.est_ancien = True
    student.annee_sortie = datetime.now().year
    student.motif_sortie = "diplômé"
    student.dernier_niveau = last_enrollment.niveau if last_enrollment else None
    
    # Créer une entrée dans l'historique
    if last_enrollment:
        history = StudentHistory(
            student_id=student.id,
            annee_academique=last_enrollment.annee_academique,
            date_debut=last_enrollment.date_inscription,
            date_fin=func.current_date(),
            statut="diplômé",
            niveau=last_enrollment.niveau,
            id_departement=last_enrollment.id_departement,
            id_parcours=last_enrollment.id_parcours,
            est_diplome=True,
            motif_fin=f"Diplômé - {type_diplome}" + (f" - Mention {mention}" if mention else ""),
            notes=f"Type de diplôme: {type_diplome}, Mention: {mention or 'N/A'}"
        )
        db.add(history)
    
    db.commit()
    db.refresh(student)
    return student


# ============ LISTER LES INSCRIPTIONS ============

def get_student_enrollments(db: Session, student_id: UUID) -> List[Enrollment]:
    """
    Récupère toutes les inscriptions d'un étudiant
    """
    return db.query(Enrollment).filter(
        Enrollment.student_id == student_id
    ).order_by(Enrollment.annee_academique.desc()).all()


# ============ INSCRIPTION MASSIVE ============

def get_enrollments_by_year_and_level(
    db: Session,
    annee_academique: str,
    niveau: str,
    admis_only: bool = True
) -> List[Enrollment]:
    """
    Récupère tous les enrollments pour une année et un niveau donnés
    """
    query = db.query(Enrollment).filter(
        Enrollment.annee_academique == annee_academique,
        Enrollment.niveau == niveau
    )
    
    if admis_only:
        query = query.filter(Enrollment.est_admis == True)
    
    return query.all()


def create_bulk_enrollments(
    db: Session,
    enrollments_data: List[dict]
) -> int:
    """
    Crée plusieurs inscriptions en masse
    Returns: nombre d'inscriptions créées
    """
    count = 0
    for data in enrollments_data:
        # Vérifier que l'étudiant n'est pas déjà inscrit
        existing = get_enrollment_by_student_and_year(
            db,
            data['student_id'],
            data['annee_academique']
        )
        
        if not existing:
            new_enrollment = Enrollment(
                student_id=data['student_id'],
                annee_academique=data['annee_academique'],
                niveau=data['niveau'],
                id_departement=data['id_departement'],
                id_parcours=data['id_parcours'],
                date_inscription=func.current_date(),
                statut="en_cours"
            )
            db.add(new_enrollment)
            count += 1
    
    db.commit()
    return count


def calculate_previous_academic_year(annee_academique: str) -> str:
    """
    Calcule l'année académique précédente
    Ex: "2024-2025" -> "2023-2024"
    """
    annee_parts = annee_academique.split("-")
    return f"{int(annee_parts[0])-1}-{int(annee_parts[1])-1}"


# ============ STATISTIQUES ============

def get_enrollment_statistics(db: Session, annee_academique: str) -> dict:
    """
    Récupère les statistiques pour une année académique
    """
    total = db.query(Enrollment).filter(
        Enrollment.annee_academique == annee_academique
    ).count()
    
    en_cours = db.query(Enrollment).filter(
        Enrollment.annee_academique == annee_academique,
        Enrollment.statut == "en_cours"
    ).count()
    
    valides = db.query(Enrollment).filter(
        Enrollment.annee_academique == annee_academique,
        Enrollment.statut == "validée"
    ).count()
    
    echoues = db.query(Enrollment).filter(
        Enrollment.annee_academique == annee_academique,
        Enrollment.statut == "échouée"
    ).count()
    
    admis = db.query(Enrollment).filter(
        Enrollment.annee_academique == annee_academique,
        Enrollment.est_admis == True
    ).count()
    
    return {
        "total": total,
        "en_cours": en_cours,
        "valides": valides,
        "echoues": echoues,
        "admis": admis,
        "taux_reussite": round((admis / total * 100) if total > 0 else 0, 2)
    }


def get_enrollment_by_level(db: Session, annee_academique: str) -> dict:
    """
    Statistiques par niveau pour une année académique
    """
    from sqlalchemy import func as sql_func
    
    results = db.query(
        Enrollment.niveau,
        sql_func.count(Enrollment.id).label('total'),
        sql_func.sum(sql_func.case((Enrollment.est_admis == True, 1), else_=0)).label('admis')
    ).filter(
        Enrollment.annee_academique == annee_academique
    ).group_by(Enrollment.niveau).all()
    
    return {
        niveau: {
            "total": total,
            "admis": admis or 0,
            "taux_reussite": round((admis / total * 100) if total > 0 and admis else 0, 2)
        }
        for niveau, total, admis in results
    }