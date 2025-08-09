from pydantic import BaseModel

class EnrEtudiant(BaseModel):
    id_etudiant: int
    nom: str
    prenom: str
    