"""
Générateur de données synthétiques pour l'entraînement du modèle.
"""
import pandas as pd
import numpy as np
from typing import List

class DataGenerator:
    """Génère un DataFrame de profils étudiants synthétiques."""

    def __init__(self, filieres: List[str]):
        self.filieres = filieres
        self.features = [
            "competence_programmation", "competence_math", "competence_physique",
            "competence_electronique", "competence_mecanique", "competence_chimie",
            "interet_aviation", "interet_informatique", "interet_donnees",
            "interet_securite", "interet_robotique", "interet_energie",
            "interet_cartographie", "interet_automobile", "trait_analytique",
            "trait_creatif", "trait_rigoureux", "trait_aventureux",
            "trait_methodique", "moyenne_math", "moyenne_physique",
            "moyenne_informatique", "moyenne_generale"
        ]

    def _generate_profile_for_filiere(self, filiere: str) -> dict:
        """Génère un profil plausible pour une filière donnée (simplifié)."""
        profile = {feat: np.random.randint(3, 8) for feat in self.features if 'moyenne' not in feat}
        profile.update({feat: np.random.uniform(8, 14) for feat in self.features if 'moyenne' in feat})

        if filiere in ["Génie Logiciel", "Intelligence Artificielle", "Big Data"]:
            profile["competence_programmation"] = np.random.randint(7, 11)
            profile["interet_informatique"] = np.random.randint(7, 11)
            profile["competence_math"] = np.random.randint(6, 11)
            profile["moyenne_informatique"] = np.random.uniform(13, 18)
        
        if filiere in ["Aéronautique", "Pilotage"]:
            profile["competence_physique"] = np.random.randint(7, 11)
            profile["interet_aviation"] = np.random.randint(8, 11)
            profile["moyenne_physique"] = np.random.uniform(12, 17)

        # Ajouter un peu de bruit
        for key in profile:
            if 'moyenne' not in key:
                profile[key] += np.random.randint(-1, 2)
                profile[key] = np.clip(profile[key], 0, 10)

        return profile

    def generate(self, n_samples: int) -> pd.DataFrame:
        """Génère le dataset complet."""
        data = []
        for _ in range(n_samples):
            target_filiere = np.random.choice(self.filieres)
            profile = self._generate_profile_for_filiere(target_filiere)
            profile['filiere_cible'] = target_filiere
            data.append(profile)
        return pd.DataFrame(data)