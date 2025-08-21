from typing import Optional


from pydantic import BaseModel, ConfigDict
from datetime import datetime

class Etudiant(BaseModel):
    id_etudiant: int
    nom: str
    prenom: str
    sexe: Optional[str] = None
    date_creation: Optional[datetime] =  None

    model_config = ConfigDict(from_attributes=True)

class EnrEtudiant(Etudiant):
    pass

    model_config = ConfigDict(from_attributes=True)

class ModifierEtudiant(BaseModel):
    nom: str
    prenom: str
    sexe: str

    model_config = ConfigDict(from_attributes=True)

