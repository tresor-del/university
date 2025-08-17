from pydantic import BaseModel

class EnrEtudiant(BaseModel):
    id_etudiant: int
    nom: str
    prenom: str

class ListeEtudiant(EnrEtudiant):
    pass

class ModifierEtudiant(BaseModel):
    nom: str
    prenom: str

