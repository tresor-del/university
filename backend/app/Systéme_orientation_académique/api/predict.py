"""
API de prédiction pour intégration avec le backend FastAPI existant
"""

from typing import List, Optional
from functools import lru_cache
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

from config import get_config
from api.schemas import StudentProfileInput, OrientationRecommendation, OrientationResponse
from src.models.rule_based import RuleBasedOrientationSystem
from src.models.ml_model import OrientationMLModel
from src.models.hybrid_system import HybridOrientationSystem

# ============================================================================
# INITIALISATION DES MODÈLES (SINGLETON)
# ============================================================================

class OrientationService:
    """Service singleton pour les modèles d'orientation"""
    
    def __init__(self):
        """Initialise les modèles en lisant la configuration."""
        try:
            config = get_config()
            models_dir = config['paths']['models_saved']
            rules_path = os.path.join(config['paths']['rules'], config['files']['rules'])
            
            # Système à règles
            self.rule_system = RuleBasedOrientationSystem(rules_path=rules_path)
            
            # Modèle ML
            self.ml_model = OrientationMLModel()
            self.ml_model.load(
                os.path.join(models_dir, config['files']['model']),
                os.path.join(models_dir, config['files']['scaler']),
                os.path.join(models_dir, config['files']['encoder'])
            )
            
            # Système hybride
            self.hybrid_system = HybridOrientationSystem(
                self.rule_system, 
                self.ml_model,
                weights=config.get('weights')
            )
            
            self.initialized = True
            print("✓ Système d'orientation initialisé avec succès")
            
        except Exception as e:
            self.initialized = False
            print(f"❌ Erreur lors de l'initialisation: {e}")
            raise
    
    def get_recommendations(self, profile: dict, top_n: int = 3) -> List[dict]:
        """Obtient les recommandations"""
        if not self.initialized:
            raise RuntimeError("Le service n'est pas initialisé")
        
        return self.hybrid_system.recommend(profile, top_n=top_n)
    

# Instance globale
@lru_cache()
def get_orientation_service():
    """Crée et retourne une instance unique du service (injection de dépendance)"""
    service = OrientationService()
    if not service.initialized:
        raise RuntimeError("Le service d'orientation n'a pas pu être initialisé.")
    return service


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
    service: OrientationService = Depends(get_orientation_service),
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
        recommendations = service.get_recommendations(
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
    service: OrientationService = Depends(get_orientation_service),
    current_user: CurrentUser,
    top_n: int = 3
) -> OrientationResponse:
    """
    Prédit et sauvegarde les recommandations pour un étudiant spécifique
    """
    # Obtenir les recommandations via le service injecté
    profile_dict = profile.model_dump()
    recommendations = service.get_recommendations(
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
async def get_available_filieres(
    current_user: CurrentUser,
    service: OrientationService = Depends(get_orientation_service)
) -> dict:
    """
    Retourne la liste des filières disponibles
    """
    filieres = list(service.rule_system.rules.keys())
    
    return {
        "filieres": filieres,
        "count": len(filieres)
    }


@router.get("/health")
async def health_check(
    service: OrientationService = Depends(get_orientation_service)
) -> dict:
    """Vérifie que le système d'orientation est opérationnel"""
    return {
        "status": "ok" if service.initialized else "error",
        "system": "Système d'orientation académique",
        "version": "1.0.0"
    }