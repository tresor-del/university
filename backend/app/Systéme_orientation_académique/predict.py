"""
API de prédiction pour intégration avec le backend FastAPI existant
"""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
import os
import sys
from pathlib import Path

# Permettre l'import depuis le dossier 'src'
# Cette ligne ajoute la racine du projet (le dossier parent de 'api') au path de Python.
# C'est nécessaire pour que les imports comme `from src.models...` fonctionnent
# lorsque ce fichier est utilisé par FastAPI.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from api.schemas import StudentProfileInput, OrientationRecommendation, OrientationResponse
from src.models.rule_based import RuleBasedOrientationSystem
from src.models.ml_model import OrientationMLModel
from src.models.hybrid_system import HybridOrientationSystem

# ============================================================================
# INITIALISATION DES MODÈLES (SINGLETON)
# ============================================================================

class OrientationService:
    """Service singleton pour les modèles d'orientation"""
    
    _instance = None
    _rule_system = None
    _ml_model = None
    _hybrid_system = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def initialize(self, models_dir: str = "models/saved", rules_path: str = "models/rules/orientation_rules.json"):
        """Initialise les modèles (appelé au démarrage de l'app)"""
        if self._initialized:
            return
        
        try:
            # Système à règles
            self._rule_system = RuleBasedOrientationSystem(rules_path=rules_path)
            
            # Modèle ML
            self._ml_model = OrientationMLModel()
            self._ml_model.load(
                os.path.join(models_dir, "orientation_model.pkl"),
                os.path.join(models_dir, "scaler.pkl"),
                os.path.join(models_dir, "label_encoder.pkl")
            )
            
            # Système hybride
            self._hybrid_system = HybridOrientationSystem(
                self._rule_system, 
                self._ml_model
            )
            
            self._initialized = True
            print("✓ Système d'orientation initialisé avec succès")
            
        except Exception as e:
            print(f"❌ Erreur lors de l'initialisation: {e}")
            raise
    
    def get_recommendations(self, profile: dict, top_n: int = 3) -> List[dict]:
        """Obtient les recommandations"""
        if not self._initialized:
            raise RuntimeError("Le service n'est pas initialisé")
        
        return self._hybrid_system.recommend(profile, top_n=top_n)
    

# Instance globale
orientation_service = OrientationService()


# ============================================================================
# ROUTES API
# ============================================================================

router = APIRouter(prefix="/orientation", tags=["Orientation"])

# Ces imports sont un exemple, vous devrez les adapter à votre backend principal
# from app.api.deps import SessionDeps, CurrentUser
CurrentUser = dict # Placeholder


@router.post("/predict", response_model=OrientationResponse)
async def predict_orientation(
    profile: StudentProfileInput,
    current_user: CurrentUser,
    top_n: int = 3
) -> OrientationResponse:
    """
    Prédit les filières recommandées pour un profil étudiant
    
    Utilise un système hybride combinant:
    - Règles expertes métier
    - Machine Learning (Random Forest)
    """
    try:
        # Convertir en dict
        profile_dict = profile.model_dump()
        
        # Obtenir les recommandations
        recommendations = orientation_service.get_recommendations(
            profile_dict, 
            top_n=top_n
        )
        
        # Les explications sont maintenant incluses directement dans les recommandations
        enriched_recs = [
            OrientationRecommendation(**rec) for rec in recommendations
        ]
        
        from datetime import datetime
        return OrientationResponse(
            recommendations=enriched_recs,
            student_id=current_user.get("id") if isinstance(current_user, dict) else None,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la prédiction: {str(e)}"
        )


@router.post("/predict/{student_id}", response_model=OrientationResponse)
async def predict_orientation_for_student(
    student_id: UUID,
    profile: StudentProfileInput,
    # db: SessionDeps, # Placeholder
    current_user: CurrentUser,
    top_n: int = 3
) -> OrientationResponse:
    """
    Prédit et sauvegarde les recommandations pour un étudiant spécifique
    """
    # Obtenir les recommandations
    profile_dict = profile.model_dump()
    recommendations = orientation_service.get_recommendations(
        profile_dict,
        top_n=top_n
    )
    
    # TODO: Sauvegarder les recommandations dans la DB si nécessaire
    
    enriched_recs = [
        OrientationRecommendation(**rec) for rec in recommendations
    ]
    
    from datetime import datetime
    return OrientationResponse(
        recommendations=enriched_recs,
        student_id=student_id,
        timestamp=datetime.now().isoformat()
    )


@router.get("/filieres")
async def get_available_filieres(current_user: CurrentUser) -> dict:
    """
    Retourne la liste des filières disponibles
    """
    filieres = list(orientation_service._rule_system.rules.keys())
    
    return {
        "filieres": filieres,
        "count": len(filieres)
    }


@router.get("/health")
async def health_check() -> dict:
    """Vérifie que le système d'orientation est opérationnel"""
    return {
        "status": "ok" if orientation_service._initialized else "not_initialized",
        "system": "Système d'orientation académique",
        "version": "1.0.0"
    }