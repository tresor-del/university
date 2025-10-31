from datetime import datetime
from typing import Optional
from app.models.student_history import StudentHistory
from fastapi import Body

import uuid
from datetime import datetime
from typing import Any, List
from uuid import UUID

from sqlalchemy import func, select

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from app.api.deps import SessionDeps, get_current_active_admin
from app.models.students import Student, StudentStatus
from app.schemas.message import Message
from app.crud.admin.services_inscription.new_students import (
    students_list as crud_students_list,
    get_pending_students,
    valider_student,
    rejeter_student,
    enroll_student as crud_enroll_student,
    update_student as crud_update_student,
    delete_student as crud_delete_student,
    get_student as crud_get_student
)
from app.schemas.students import StudentResponse, StudentUpdate, StudentCreate, StudentsResponse

router = APIRouter(prefix="/students", tags=["Students"])


# ============ MARQUER COMME ANCIEN ÉTUDIANT ============

@router.post("/{student_id}/marquer-comme-ancien", dependencies=[Depends(get_current_active_admin)])
def marquer_comme_ancien(
    student_id: UUID,
    annee_sortie: int = Body(...),
    motif_sortie: str = Body(...),  # diplômé, abandon, transfert, exclusion
    dernier_niveau: Optional[str] = Body(None),
    est_diplome: bool = Body(False),
    db: SessionDeps = Depends()
) -> Message:
    """
    Marque un étudiant comme ancien (fin d'études, abandon, diplômé, etc.)
    """
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")
    
    if student.statut not in [StudentStatus.ACTIF, StudentStatus.SUSPENDU]:
        raise HTTPException(
            status_code=400,
            detail=f"Seuls les étudiants actifs peuvent être archivés (statut actuel: {student.statut})"
        )
    
    # Créer l'entrée dans l'historique
    history = StudentHistory(
        student_id=student.id,
        annee_academique=f"{annee_sortie-1}-{annee_sortie}",
        date_debut=student.date_inscription,
        date_fin=func.current_date(),
        statut=motif_sortie,
        niveau=dernier_niveau,
        id_departement=student.id_departement,
        id_parcours=student.id_parcours,
        est_diplome=est_diplome,
        motif_fin=motif_sortie
    )
    db.add(history)
    
    # Mettre à jour l'étudiant
    student.est_ancien = True
    student.statut = StudentStatus.ANCIEN
    student.annee_sortie = annee_sortie
    student.motif_sortie = motif_sortie
    student.dernier_niveau = dernier_niveau
    
    db.commit()
    
    return Message(message=f"Étudiant marqué comme ancien ({motif_sortie})")


# ============ LISTER LES ANCIENS ÉTUDIANTS ============

@router.get("/anciens", dependencies=[Depends(get_current_active_admin)])
def get_anciens_students(
    db: SessionDeps,
    skip: int = 0,
    limit: int = 100,
    annee_sortie: Optional[int] = None,
    motif_sortie: Optional[str] = None,
    diplomes_uniquement: bool = False
) -> StudentsResponse:
    """
    Liste tous les anciens étudiants avec filtres optionnels
    """
    query = db.query(Student).filter(Student.est_ancien == True)
    
    if annee_sortie:
        query = query.filter(Student.annee_sortie == annee_sortie)
    
    if motif_sortie:
        query = query.filter(Student.motif_sortie == motif_sortie)
    
    if diplomes_uniquement:
        query = query.join(StudentHistory).filter(StudentHistory.est_diplome == True)
    
    count = query.count()
    students = query.offset(skip).limit(limit).all()
    
    return StudentsResponse(data=students, count=count)


# ============ RÉINSCRIPTION D'UN ANCIEN ÉTUDIANT ============

@router.post("/{student_id}/reinscription", dependencies=[Depends(get_current_active_admin)])
def reinscription_ancien_student(
    student_id: UUID,
    nouveau_parcours_id: Optional[int] = Body(None),
    nouveau_departement_id: Optional[int] = Body(None),
    notes: Optional[str] = Body(None),
    db: SessionDeps = Depends()
) -> StudentResponse:
    """
    Réinscrit un ancien étudiant pour une nouvelle année académique
    """
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")
    
    if not student.est_ancien:
        raise HTTPException(
            status_code=400,
            detail="Cet étudiant n'est pas marqué comme ancien"
        )
    
    # Vérifier si l'étudiant peut se réinscrire
    if student.motif_sortie == "exclusion":
        raise HTTPException(
            status_code=403,
            detail="Les étudiants exclus ne peuvent pas se réinscrire"
        )
    
    # Mettre à jour les informations
    if nouveau_parcours_id:
        student.id_parcours = nouveau_parcours_id
    if nouveau_departement_id:
        student.id_departement = nouveau_departement_id
    
    # Réinitialiser le statut
    student.statut = StudentStatus.VALIDE  # Ou EN_ATTENTE si besoin de validation
    student.nombre_reinscriptions += 1
    student.date_derniere_reinscription = func.current_date()
    
    # Créer une nouvelle entrée dans l'historique
    annee_actuelle = datetime.now().year
    new_history = StudentHistory(
        student_id=student.id,
        annee_academique=f"{annee_actuelle}-{annee_actuelle+1}",
        date_debut=func.current_date(),
        statut="réinscription",
        niveau=student.dernier_niveau or "À définir",
        id_departement=student.id_departement,
        id_parcours=student.id_parcours,
        notes=notes
    )
    db.add(new_history)
    
    db.commit()
    db.refresh(student)
    
    return student


# ============ DEMANDE DE RÉINSCRIPTION PAR L'ÉTUDIANT ============

@router.post("/demande-reinscription/{student_id}")
def demander_reinscription(
    student_id: UUID,
    nouveau_parcours_id: Optional[int] = Body(None),
    motif_reinscription: str = Body(...),
    db: SessionDeps = Depends()
) -> Message:
    """
    Permet à un ancien étudiant de demander sa réinscription (route publique)
    Le dossier sera en attente de validation par un admin
    """
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")
    
    if not student.est_ancien:
        raise HTTPException(
            status_code=400,
            detail="Cette route est réservée aux anciens étudiants"
        )
    
    if student.statut == StudentStatus.REINSCRIPTION_EN_ATTENTE:
        raise HTTPException(
            status_code=400,
            detail="Une demande de réinscription est déjà en cours"
        )
    
    # Mettre le statut en attente de validation
    student.statut = StudentStatus.REINSCRIPTION_EN_ATTENTE
    if nouveau_parcours_id:
        student.id_parcours = nouveau_parcours_id
    
    # Enregistrer le motif dans les notes
    student.motif_rejet = motif_reinscription  # Réutiliser ce champ temporairement
    
    db.commit()
    
    return Message(
        message="Votre demande de réinscription a été soumise. Un admin la traitera prochainement."
    )


# ============ VALIDER UNE DEMANDE DE RÉINSCRIPTION ============

@router.post("/{student_id}/valider-reinscription", dependencies=[Depends(get_current_active_admin)])
def valider_reinscription(
    student_id: UUID,
    db: SessionDeps = Depends(),
    current_admin = Depends(get_current_active_admin)
) -> StudentResponse:
    """
    Valide une demande de réinscription d'un ancien étudiant
    """
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")
    
    if student.statut != StudentStatus.REINSCRIPTION_EN_ATTENTE:
        raise HTTPException(
            status_code=400,
            detail="Aucune demande de réinscription en attente pour cet étudiant"
        )
    
    # Valider la réinscription
    student.statut = StudentStatus.VALIDE
    student.nombre_reinscriptions += 1
    student.date_derniere_reinscription = func.current_date()
    student.date_validation = func.now()
    student.valide_par_admin_id = current_admin.id
    
    # Créer l'historique
    annee_actuelle = datetime.now().year
    new_history = StudentHistory(
        student_id=student.id,
        annee_academique=f"{annee_actuelle}-{annee_actuelle+1}",
        date_debut=func.current_date(),
        statut="réinscription_validée",
        niveau=student.dernier_niveau or "À définir",
        id_departement=student.id_departement,
        id_parcours=student.id_parcours,
        notes=f"Réinscription validée par admin. Motif: {student.motif_rejet}"
    )
    db.add(new_history)
    
    # Nettoyer le champ temporaire
    student.motif_rejet = None
    
    db.commit()
    db.refresh(student)
    
    # TODO: Envoyer email de confirmation
    
    return student


# ============ HISTORIQUE D'UN ÉTUDIANT ============

@router.get("/{student_id}/historique", dependencies=[Depends(get_current_active_admin)])
def get_student_history(student_id: UUID, db: SessionDeps) -> List[dict]:
    """
    Récupère l'historique complet des inscriptions d'un étudiant
    """
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")
    
    history = db.query(StudentHistory).filter(
        StudentHistory.student_id == student_id
    ).order_by(StudentHistory.date_debut.desc()).all()
    
    return [
        {
            "id": h.id,
            "annee_academique": h.annee_academique,
            "date_debut": h.date_debut,
            "date_fin": h.date_fin,
            "statut": h.statut,
            "niveau": h.niveau,
            "departement_id": h.id_departement,
            "parcours_id": h.id_parcours,
            "est_diplome": h.est_diplome,
            "motif_fin": h.motif_fin,
            "notes": h.notes
        }
        for h in history
    ]


# ============ RECHERCHER UN ANCIEN ÉTUDIANT ============

@router.get("/anciens/rechercher", dependencies=[Depends(get_current_active_admin)])
def rechercher_ancien_student(
    email: Optional[str] = None,
    nom: Optional[str] = None,
    id_etudiant: Optional[str] = None,
    db: SessionDeps = Depends()
) -> List[StudentResponse]:
    """
    Recherche un ancien étudiant par email, nom ou ID étudiant
    """
    query = db.query(Student).filter(Student.est_ancien == True)
    
    if email:
        query = query.filter(Student.email.ilike(f"%{email}%"))
    if nom:
        query = query.filter(
            (Student.nom.ilike(f"%{nom}%")) | (Student.prenom.ilike(f"%{nom}%"))
        )
    if id_etudiant:
        query = query.filter(Student.id_etudiant == id_etudiant)
    
    students = query.limit(50).all()
    return students


# ============ STATISTIQUES SUR LES ANCIENS ============

@router.get("/anciens/statistiques", dependencies=[Depends(get_current_active_admin)])
def stats_anciens_students(db: SessionDeps) -> dict:
    """
    Retourne des statistiques sur les anciens étudiants
    """
    total_anciens = db.query(Student).filter(Student.est_ancien == True).count()
    
    diplomes = db.query(Student).join(StudentHistory).filter(
        Student.est_ancien == True,
        StudentHistory.est_diplome == True
    ).count()
    
    abandons = db.query(Student).filter(
        Student.est_ancien == True,
        Student.motif_sortie == "abandon"
    ).count()
    
    transferts = db.query(Student).filter(
        Student.est_ancien == True,
        Student.motif_sortie == "transfert"
    ).count()
    
    reinscriptions = db.query(Student).filter(
        Student.nombre_reinscriptions > 0
    ).count()
    
    return {
        "total_anciens": total_anciens,
        "diplomes": diplomes,
        "abandons": abandons,
        "transferts": transferts,
        "reinscriptions": reinscriptions,
        "taux_diplome": round((diplomes / total_anciens * 100) if total_anciens > 0 else 0, 2)
    }