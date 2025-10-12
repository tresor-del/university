"""
Schémas Pydantic pour la validation des données de l'API.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from uuid import UUID

class StudentProfileInput(BaseModel):
    """Schéma pour le profil étudiant en entrée."""
    competence_programmation: int = Field(..., ge=0, le=10)
    competence_math: int = Field(..., ge=0, le=10)
    competence_physique: int = Field(..., ge=0, le=10)
    competence_electronique: int = Field(..., ge=0, le=10)
    competence_mecanique: int = Field(..., ge=0, le=10)
    competence_chimie: int = Field(..., ge=0, le=10)
    interet_aviation: int = Field(..., ge=0, le=10)
    interet_informatique: int = Field(..., ge=0, le=10)
    interet_donnees: int = Field(..., ge=0, le=10)
    interet_securite: int = Field(..., ge=0, le=10)
    interet_robotique: int = Field(..., ge=0, le=10)
    interet_energie: int = Field(..., ge=0, le=10)
    interet_cartographie: int = Field(..., ge=0, le=10)
    interet_automobile: int = Field(..., ge=0, le=10)
    trait_analytique: int = Field(..., ge=0, le=10)
    trait_creatif: int = Field(..., ge=0, le=10)
    trait_rigoureux: int = Field(..., ge=0, le=10)
    trait_aventureux: int = Field(..., ge=0, le=10)
    trait_methodique: int = Field(..., ge=0, le=10)
    moyenne_math: float = Field(..., ge=0, le=20)
    moyenne_physique: float = Field(..., ge=0, le=20)
    moyenne_informatique: float = Field(..., ge=0, le=20)
    moyenne_generale: float = Field(..., ge=0, le=20)

class OrientationRecommendation(BaseModel):
    """Schéma pour une seule recommandation."""
    filiere: str
    score_final: float
    confiance: str
    score_regles: float
    score_ml: float
    points_forts: Optional[List[str]] = None
    points_faibles: Optional[List[str]] = None

class OrientationResponse(BaseModel):
    """Schéma pour la réponse complète de l'API."""
    recommendations: List[OrientationRecommendation]
    student_id: Optional[UUID] = None
    timestamp: str