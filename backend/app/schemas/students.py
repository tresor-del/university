from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import datetime, date

from uuid import UUID


class StudentBase(BaseModel):
    """
    Base commun a tous les shémas
    """
    id: UUID
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
    nom_du_pere: Optional[str] = None
    nom_de_la_mere: Optional[str] = None
    addresse_du_pere: Optional[str] = None
    addresse_de_la_mere: Optional[str] = None
    nom_parent_tuteur: Optional[str] = None
    telephone_parent_tuteur: Optional[str] = None
    adresse_parent_tuteur: Optional[str] = None
    medias: Optional[list] = []

    model_config = ConfigDict(from_attributes=True)

class StudentPreInscription(BaseModel):
    """Schéma pour la pré-inscription (champs minimum requis)"""
    nom: str = Field(..., min_length=2, max_length=100)
    prenom: str = Field(..., min_length=2, max_length=100)
    date_naissance: date
    lieu_naissance: str
    sexe: str = Field(..., pattern="^(Masculin|Féminin|Autre)$")
    nationalite: str
    email: EmailStr
    telephone: str = Field(..., pattern="^[0-9+\-\s()]+$")
    adresse: Optional[str] = None
    id_departement: Optional[int] = None
    id_parcours: Optional[int] = None

class StudentCreate(StudentPreInscription):
    """Schéma pour création directe par admin (tous les champs)"""
    nom_du_pere: Optional[str] = None
    nom_de_la_mere: Optional[str] = None
    addresse_du_pere: Optional[str] = None
    addresse_de_la_mere: Optional[str] = None
    nom_parent_tuteur: Optional[str] = None
    telephone_parent_tuteur: Optional[str] = None
    adresse_parent_tuteur: Optional[str] = None
    
    
class StudentResponse(StudentBase):
    medias: Optional[list] = []

class StudentsResponse(BaseModel):
    data: List[StudentResponse]
    count: int
    
    model_config = ConfigDict(from_attributes=True)


class StudentUpdate(BaseModel):
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
    email: Optional[EmailStr] = None
    telephone: Optional[str] = None
    nom_du_pere: Optional[str] = None
    nom_de_la_mere: Optional[str] = None
    addresse_du_pere: Optional[str] = None
    addresse_de_la_mere: Optional[str] = None
    nom_parent_tuteur: Optional[str] = None
    telephone_parent_tuteur: Optional[str] = None
    adresse_parent_tuteur: Optional[str] = None
    statut: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

