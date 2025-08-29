from typing import Optional


from pydantic import BaseModel, ConfigDict
from datetime import datetime

class Student(BaseModel):
    id: int
    id_etudiant: str
    nom: str
    prenom: str
    sexe: Optional[str] = None
    date_creation: Optional[datetime] =  None

    model_config = ConfigDict(from_attributes=True)

class PublicStudent(BaseModel):
    nom: str
    prenom: str
    sexe: Optional[str] = None
    date_creation: Optional[datetime] =  None

    model_config = ConfigDict(from_attributes=True)
    
    
class EnrollStudent(BaseModel):
    nom: str
    prenom: str
    sexe: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class UpdateStudent(BaseModel):
    nom: str
    prenom: str
    sexe: str

    model_config = ConfigDict(from_attributes=True)

