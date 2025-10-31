import uuid
from datetime import datetime
from typing import Any, List, Optional
from uuid import UUID

from sqlalchemy import func, select

from fastapi import APIRouter, Depends, status, Body
from fastapi.exceptions import HTTPException

from app.api.deps import SessionDeps, get_current_active_admin
from app.models.students import Student, StudentStatus
from app.models.enrollments import Enrollment
from app.models.student_history import StudentHistory
from app.schemas.message import Message
from app.crud.admin.services_inscription.enrollments import (
    create_enrollment,
    update_student_academic_info,
    close_enrollment,
    mark_student_as_graduated
)

router = APIRouter(prefix="/students", tags=["Students"])


# ============ INSCRIRE POUR NOUVELLE ANNÉE ACADÉMIQUE ============

@router.post("/{student_id}/nouvelle-annee", dependencies=[Depends(get_current_active_admin)])
def inscrire_nouvelle_annee(
    student_id: UUID,
    annee_academique: str = Body(...),  # "2024-2025"
    nouveau_niveau: str = Body(...),  # L2, L3, M1, etc.
    id_parcours: Optional[int] = Body(None),
    id_departement: Optional[int] = Body(None),
    db: SessionDeps = Depends()
) -> dict:
    """
    Inscrit un étudiant pour une nouvelle année académique (passage en année supérieure)
    """
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")
    
    if student.statut != StudentStatus.ACTIF:
        raise HTTPException(
            status_code=400,
            detail=f"Seuls les étudiants actifs peuvent être inscrits (statut: {student.statut})"
        )
    
    # Vérifier qu'il n'a pas déjà une inscription pour cette année
    existing_enrollment = db.query(Enrollment).filter(
        Enrollment.student_id == student_id,
        Enrollment.annee_academique == annee_academique
    ).first()
    
    if existing_enrollment:
        raise HTTPException(
            status_code=400,
            detail=f"L'étudiant est déjà inscrit pour l'année {annee_academique}"
        )
    
    # Créer la nouvelle inscription
    new_enrollment = create_enrollment(
        db=db,
        student_id=student_id,
        annee_academique=annee_academique,
        id_departement=id_departement,
        id_parcours=id_parcours,
        niveau=nouveau_niveau
    )
    
    # Mettre à jour les infos de l'étudiant si changement de parcours/département
    update_student_academic_info(
        db=db,
        student_id=student_id,
        id_parcours=id_parcours,
        id_departement=id_departement
    )
    
    return {
        "message": f"Étudiant inscrit en {nouveau_niveau} pour {annee_academique}",
        "enrollment": {
            "id": new_enrollment.id,
            "annee_academique": new_enrollment.annee_academique,
            "niveau": new_enrollment.niveau
        }
    }


# ============ CLÔTURER UNE ANNÉE ACADÉMIQUE ============

@router.post("/enrollments/{enrollment_id}/cloturer", dependencies=[Depends(get_current_active_admin)])
def cloturer_annee(
    enrollment_id: int,
    est_admis: bool = Body(...),
    moyenne_annuelle: Optional[float] = Body(None),
    credits_obtenus: int = Body(0),
    db: SessionDeps = Depends()
) -> Message:
    """
    Clôture une année académique pour un étudiant (saisie des résultats)
    """
    enrollment = db.get(Enrollment, enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Inscription non trouvée")
    
    if enrollment.statut != "en_cours":
        raise HTTPException(
            status_code=400,
            detail=f"Cette inscription est déjà clôturée (statut: {enrollment.statut})"
        )
    
    # Mettre à jour les résultats
    close_enrollment(
        db=db,
        enrollment_id=enrollment_id, 
        est_admis=est_admis,
        moyenne_annuelle=moyenne_annuelle,
        credits_obtenus=credits_obtenus
    )
    
    return Message(
        message=f"Année académique clôturée. Étudiant {'admis' if est_admis else 'non admis'} en année supérieure"
    )


# ============ DIPLÔMER UN ÉTUDIANT ============

@router.post("/{student_id}/diplomer", dependencies=[Depends(get_current_active_admin)])
def diplomer_student(
    student_id: UUID,
    type_diplome: str = Body(...),  # "Licence", "Master", etc.
    mention: Optional[str] = Body(None),  # "Passable", "Assez bien", "Bien", "Très bien"
    db: SessionDeps = Depends()
) -> dict:
    """
    Marque un étudiant comme diplômé (devient un ancien)
    """
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")
    
    if student.statut != StudentStatus.ACTIF:
        raise HTTPException(
            status_code=400,
            detail="Seuls les étudiants actifs peuvent être diplômés"
        )
    
    # Récupérer la dernière inscription
    last_enrollment = db.query(Enrollment).filter(
        Enrollment.student_id == student_id
    ).order_by(Enrollment.date_inscription.desc()).first()
    
    if last_enrollment:
        last_enrollment.statut = "validée"
        last_enrollment.est_admis = True
    
    # Marquer comme ancien
    mark_student_as_graduated(
        db=db,
        student_id=student_id,
        type_diplome=type_diplome,
        mention=mention
    )
    
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
    
    return {
        "message": f"Étudiant diplômé avec succès ({type_diplome})",
        "student": {
            "id": student.id,
            "id_etudiant": student.id_etudiant,
            "nom_complet": f"{student.prenom} {student.nom}",
            "statut": student.statut,
            "type_diplome": type_diplome,
            "mention": mention
        }
    }


# ============ LISTER LES INSCRIPTIONS D'UN ÉTUDIANT ============

@router.get("/{student_id}/inscriptions", dependencies=[Depends(get_current_active_admin)])
def get_student_enrollments(student_id: UUID, db: SessionDeps) -> List[dict]:
    """
    Récupère toutes les inscriptions annuelles d'un étudiant
    """
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")
    
    enrollments = db.query(Enrollment).filter(
        Enrollment.student_id == student_id
    ).order_by(Enrollment.annee_academique.desc()).all()
    
    return [
        {
            "id": e.id,
            "annee_academique": e.annee_academique,
            "niveau": e.niveau,
            "statut": e.statut,
            "moyenne": e.moyenne_annuelle,
            "credits": e.credits_obtenus,
            "est_admis": e.est_admis,
            "departement_id": e.id_departement,
            "parcours_id": e.id_parcours
        }
        for e in enrollments
    ]


# ============ INSCRIPTION MASSIVE POUR NOUVELLE ANNÉE ============

@router.post("/inscriptions-massives", dependencies=[Depends(get_current_active_admin)])
def inscription_massive_nouvelle_annee(
    annee_academique: str = Body(...),
    niveau_source: str = Body(...),  # "L1" (ceux qui étaient en L1)
    niveau_destination: str = Body(...),  # "L2" (où ils vont)
    admis_seulement: bool = Body(True),  # Inscrire seulement ceux qui ont réussi
    db: SessionDeps = Depends()
) -> dict:
    """
    Inscrit massivement tous les étudiants admis d'un niveau pour l'année suivante
    """
    # Récupérer l'année académique précédente
    annee_parts = annee_academique.split("-")
    annee_precedente = f"{int(annee_parts[0])-1}-{int(annee_parts[1])-1}"
    
    # Récupérer tous les enrollments de l'année précédente pour ce niveau
    enrollments_precedents = db.query(Enrollment).filter(
        Enrollment.annee_academique == annee_precedente,
        Enrollment.niveau == niveau_source
    )
    
    if admis_seulement:
        enrollments_precedents = enrollments_precedents.filter(Enrollment.est_admis == True)
    
    enrollments_precedents = enrollments_precedents.all()
    
    inscriptions_creees = 0
    for old_enrollment in enrollments_precedents:
        # Vérifier que l'étudiant n'est pas déjà inscrit
        existing = db.query(Enrollment).filter(
            Enrollment.student_id == old_enrollment.student_id,
            Enrollment.annee_academique == annee_academique
        ).first()
        
        if not existing:
            new_enrollment = Enrollment(
                student_id=old_enrollment.student_id,
                annee_academique=annee_academique,
                niveau=niveau_destination,
                id_departement=old_enrollment.id_departement,
                id_parcours=old_enrollment.id_parcours,
                date_inscription=func.current_date(),
                statut="en_cours"
            )
            db.add(new_enrollment)
            inscriptions_creees += 1
    
    db.commit()
    
    return {
        "message": f"{inscriptions_creees} étudiants inscrits en {niveau_destination} pour {annee_academique}",
        "nombre_inscriptions": inscriptions_creees
    }