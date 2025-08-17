from typing import Optional

from pydantic import BaseModel
from datetime import datetime

class EnrEtudiant(BaseModel):
    id_etudiant: int
    nom: str
    prenom: str
    sexe: Optional[str] = None
    date_creation: Optional[datetime] =  None


class ModifierEtudiant(BaseModel):
    nom: str
    prenom: str


    class Config:
        orm_mode = True

