"""
Système hybride combinant les règles expertes et le Machine Learning.
"""
from typing import List, Dict, Any
from .rule_based import RuleBasedOrientationSystem
from .ml_model import OrientationMLModel

class HybridOrientationSystem:
    """
    Combine les scores du système à règles et du modèle ML pour une recommandation finale.
    """

    def __init__(self, rule_system: RuleBasedOrientationSystem, ml_model: OrientationMLModel, weights: Dict[str, float] = None):
        """
        Initialise le système hybride.

        Args:
            rule_system: Instance du système à règles.
            ml_model: Instance du modèle ML.
            weights (Dict): Pondérations pour 'rules' et 'ml'.
        """
        self.rule_system = rule_system
        self.ml_model = ml_model
        self.weights = weights or {'rules': 0.4, 'ml': 0.6}

    def recommend(self, profile: Dict[str, Any], top_n: int = 3) -> List[Dict[str, Any]]:
        """
        Génère des recommandations hybrides.
        """
        # Obtenir les recommandations des deux systèmes
        rule_recs = self.rule_system.recommend(profile, top_n=len(self.rule_system.rules))
        ml_recs = self.ml_model.predict(profile, top_n=len(self.rule_system.rules))

        # Convertir en dictionnaires pour un accès facile
        rule_scores = {rec['filiere']: rec['score'] for rec in rule_recs}
        ml_scores = {rec['filiere']: rec['confidence'] for rec in ml_recs}

        # Calculer le score final pondéré
        final_scores = {}
        all_filieres = set(rule_scores.keys()) | set(ml_scores.keys())

        for filiere in all_filieres:
            score_regles = rule_scores.get(filiere, 0)
            score_ml = ml_scores.get(filiere, 0)

            # Ne pas recommander si éliminé par les règles
            if score_regles == 0 and rule_scores.get(filiere) is not None:
                continue

            score_final = (score_regles * self.weights['rules']) + (score_ml * self.weights['ml'])
            
            confiance = "Faible"
            if score_final >= 75: confiance = "Très élevée"
            elif score_final >= 60: confiance = "Élevée"
            elif score_final >= 45: confiance = "Moyenne"

            final_scores[filiere] = {
                "score_final": round(score_final, 2),
                "confiance": confiance,
                "details": {
                    "score_regles": score_regles,
                    "score_ml": score_ml,
                }
            }

        # Trier et formater la sortie
        sorted_recs = sorted(final_scores.items(), key=lambda item: item[1]['score_final'], reverse=True)

        recommendations = []
        for filiere, scores in sorted_recs[:top_n]:
            recommendations.append({
                "filiere": filiere,
                "score_final": scores['score_final'],
                "confiance": scores['confiance'],
                **scores['details']
            })

        return recommendations