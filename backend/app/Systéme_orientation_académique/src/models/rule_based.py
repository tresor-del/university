"""
Système d'orientation basé sur des règles expertes.
"""
import json
from typing import List, Dict, Any

class RuleBasedOrientationSystem:
    """
    Évalue le profil d'un étudiant en fonction d'un ensemble de règles
    définies dans un fichier JSON.
    """

    def __init__(self, rules_path: str):
        """
        Initialise le système en chargeant les règles.

        Args:
            rules_path (str): Chemin vers le fichier JSON des règles.
        """
        try:
            with open(rules_path, 'r', encoding='utf-8') as f:
                self.rules = json.load(f)
            print(f"✓ Règles chargées depuis {rules_path}")
        except FileNotFoundError:
            print(f"❌ Fichier de règles introuvable: {rules_path}")
            raise
        except json.JSONDecodeError:
            print(f"❌ Erreur de décodage JSON dans {rules_path}")
            raise

    def _evaluate_rule(self, profile: Dict[str, Any], rule: Dict[str, Any]) -> bool:
        """Évalue une seule condition de règle."""
        feature = rule['feature']
        operator = rule['operator']
        value = rule['value']
        profile_value = profile.get(feature, 0)

        if operator == '>=':
            return profile_value >= value
        if operator == '<=':
            return profile_value <= value
        if operator == '==':
            return profile_value == value
        # Ajoutez d'autres opérateurs si nécessaire
        return False

    def recommend(self, profile: Dict[str, Any], top_n: int = 3) -> List[Dict[str, Any]]:
        """
        Recommande des filières en fonction du profil de l'étudiant.

        Args:
            profile (Dict[str, Any]): Le profil de l'étudiant.
            top_n (int): Le nombre de meilleures recommandations à retourner.

        Returns:
            List[Dict[str, Any]]: Une liste de dictionnaires contenant les recommandations.
        """
        scores = {}
        for filiere, criteria in self.rules.items():
            score = 0
            total_weight = 0
            
            # Vérifier les critères requis
            required_met = all(self._evaluate_rule(profile, rule) for rule in criteria.get('required', []))
            if not required_met:
                scores[filiere] = {'score': 0, 'confidence': 'Éliminatoire', 'raison': 'Critères requis non satisfaits'}
                continue

            # Calculer le score basé sur les autres critères
            for category in ['preferred', 'bonus']:
                for rule in criteria.get(category, []):
                    weight = 3 if category == 'preferred' else 1 # Poids arbitraire
                    total_weight += weight
                    if self._evaluate_rule(profile, rule):
                        score += weight
            
            # Normaliser le score sur 100
            normalized_score = (score / total_weight) * 100 if total_weight > 0 else 0
            
            scores[filiere] = {
                'score': round(normalized_score),
                'confidence': 'Élevée' if normalized_score > 70 else 'Moyenne',
                'raison': 'Basé sur les compétences et intérêts correspondants.'
            }

        # Trier les filières par score
        sorted_filieres = sorted(scores.items(), key=lambda item: item[1]['score'], reverse=True)

        recommendations = [{'filiere': f, **s} for f, s in sorted_filieres[:top_n]]
        return recommendations