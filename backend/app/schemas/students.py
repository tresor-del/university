from typing import Optional

from pydantic import BaseModel, ConfigDict
from datetime import datetime, date



class StudentBase(BaseModel):
    """
    Base commun a tous les shémas
    """
    id: int
    id_etudiant: str
    nom: str
    prenom: str
    sexe: Optional[str] = None
    date_naissance: Optional[date] = None
    lieu_naissance: Optional[str] = None
    nationalite: Optional[str] = None
    adresse: Optional[str] = None
    email: Optional[str] = None
    telephone: Optional[str] = None
    nom_parent_tuteur: Optional[str] = None
    telephone_parent_tuteur: Optional[str] = None
    adresse_parent_tuteur: Optional[str] = None
    photo: Optional[str] = None
    statut: Optional[str] = "actif"

    model_config = ConfigDict(from_attributes=True)


class EnrollStudent(BaseModel):
    """
    Shéma pour inscrire un étudiant
    """
    nom: str
    prenom: str
    sexe: Optional[str] = None
    date_naissance: Optional[date] = None
    lieu_naissance: Optional[str] = None
    nationalite: Optional[str] = None
    adresse: Optional[str] = None
    email: Optional[str] = None
    telephone: Optional[str] = None
    nom_parent_tuteur: Optional[str] = None
    telephone_parent_tuteur: Optional[str] = None
    adresse_parent_tuteur: Optional[str] = None
    id_departement: Optional[str] = None
    id_parcours: Optional[str] = None
    photo: Optional[str] = None
    qr: Optional[str] = None
    statut: Optional[str] = "actif"

    model_config = ConfigDict(from_attributes=True)

class PublicStudent(BaseModel):
    """
    Shema pour lecture publique
    """
    nom: str
    prenom: str
    sexe: Optional[str] = None
    classe_actuelle_id: Optional[int] = None
    date_creation: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class StudentModel(StudentBase):
    """
    Shema pour lecture complète
    """
    date_inscription: Optional[date] = None
    classe_actuelle_id: Optional[int] = None
    date_creation: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class UpdateStudent(BaseModel):
    """
    Shema pour mise a jour
    """
    nom: Optional[str] = None
    prenom: Optional[str] = None
    sexe: Optional[str] = None
    date_naissance: Optional[date] = None
    lieu_naissance: Optional[str] = None
    nationalite: Optional[str] = None
    adresse: Optional[str] = None
    email: Optional[str] = None
    telephone: Optional[str] = None
    nom_parent_tuteur: Optional[str] = None
    telephone_parent_tuteur: Optional[str] = None
    adresse_parent_tuteur: Optional[str] = None
    photo: Optional[str] = None
    qr: Optional[str] = None
    statut: Optional[str] = None
    classe_actuelle_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
