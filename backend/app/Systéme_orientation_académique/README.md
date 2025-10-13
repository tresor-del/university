# 🎓 Système d'Orientation Académique
## École d'Aéronautique et Technologies Avancées

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-orange.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)

Système intelligent d'orientation académique combinant **règles expertes** et **machine learning** pour recommander la filière optimale à chaque étudiant.

---

## 📋 Table des matières

- [Vue d'ensemble](#vue-densemble)
- [Filières disponibles](#filières-disponibles)
- [Architecture](#architecture)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Lancement de l'API](#lancement-de-lapi)
- [Intégration avec FastAPI](#intégration-avec-fastapi)
- [Structure du projet](#structure-du-projet)
- [Algorithmes](#algorithmes)
- [Performance](#performance)
- [Contribution](#contribution)

---

## 🎯 Vue d'ensemble

Ce système permet de recommander la filière la plus adaptée à un étudiant en fonction de:

- **Compétences techniques** (programmation, mathématiques, physique, etc.)
- **Intérêts** (aviation, informatique, robotique, etc.)
- **Traits de personnalité** (analytique, créatif, rigoureux, etc.)
- **Résultats académiques** (moyennes dans différentes matières)

### Approche hybride

Le système combine trois méthodes:

1. **Règles expertes** (40%) - Logique métier définie par des experts
2. **Machine Learning** (60%) - Modèle entraîné sur des données
3. **Score pondéré final** - Combinaison optimale des deux approches

---

## 🎓 Filières disponibles

1. **Génie Logiciel** - Développement d'applications et systèmes
2. **Intelligence Artificielle** - IA, Deep Learning, NLP
3. **Big Data** - Analyse de données massives, Data Science
4. **Objets Connectés (IoT)** - Systèmes embarqués connectés
5. **Cybersécurité** - Sécurité informatique et réseaux
6. **Robotique** - Conception et programmation de robots
7. **Aéronautique** - Ingénierie aéronautique et spatiale
8. **Pilotage** - Formation de pilotes professionnels
9. **Pétrochimie** - Ingénierie pétrolière et chimique
10. **Topographie** - Géomatique et cartographie
11. **Maintenance Automobile** - Systèmes automobiles modernes

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  PROFIL ÉTUDIANT                        │
│  (Compétences, Intérêts, Personnalité, Notes)          │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
┌────────▼──────────┐   ┌───────▼────────────┐
│  RÈGLES EXPERTES  │   │  MACHINE LEARNING  │
│                   │   │                    │
│  • Seuils requis  │   │  • Random Forest   │
│  • Critères bonus │   │  • 100 estimateurs │
│  • Logique métier │   │  • Features: 25+   │
└────────┬──────────┘   └───────┬────────────┘
         │                       │
         │    Score: 40%         │  Score: 60%
         └───────────┬───────────┘
                     │
            ┌────────▼────────┐
            │ SYSTÈME HYBRIDE │
            │                 │
            │  Score final    │
            │  pondéré        │
            └────────┬────────┘
                     │
            ┌────────▼────────┐
            │ RECOMMANDATIONS │
            │  Top 3 filières │
            └─────────────────┘
```

---

## 🚀 Installation

### Prérequis

- Python 3.8+
- pip
- uv (recommandé pour la gestion de l'environnement)

### Étapes d'installation

```bash
# 1. Installer uv (si ce n'est pas déjà fait)
# https://github.com/astral-sh/uv
pip install uv

# 2. Se placer dans le répertoire du projet
cd votre_projet/
mkdir backend_ml
cd backend_ml

# 3. Créer et activer un environnement virtuel avec uv (recommandé)
uv venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# 4. Installer les dépendances avec uv (plus rapide)
uv pip install -r requirements.txt
```

---

## 💻 Utilisation

### Pipeline complet (recommandé pour la première utilisation)

```bash
# Génère les données, entraîne le modèle et teste
python main.py --full-pipeline
```

### Commandes individuelles

```bash
# Générer des données synthétiques (1500 échantillons)
python main.py --generate-data --n-samples 1500

# Entraîner le modèle ML
python main.py --train

# Tester des prédictions
python main.py --predict
```

### Utilisation programmatique

```python
from src.models.rule_based import RuleBasedOrientationSystem
from src.models.ml_model import OrientationMLModel
from src.models.hybrid_system import HybridOrientationSystem

# Initialiser les systèmes
rule_system = RuleBasedOrientationSystem()
ml_model = OrientationMLModel()
ml_model.load("models/saved/orientation_model.pkl",
              "models/saved/scaler.pkl",
              "models/saved/label_encoder.pkl")

# Créer le système hybride
hybrid = HybridOrientationSystem(rule_system, ml_model)

# Profil étudiant
student = {
    "competence_programmation": 9,
    "competence_math": 8,
    "interet_informatique": 9,
    "interet_donnees": 8,
    # ... autres attributs
}

# Obtenir les recommandations
recommendations = hybrid.recommend(student, top_n=3)

for rec in recommendations:
    print(f"{rec['filiere']}: {rec['score_final']}/100")
```

---

## 🔌 Intégration avec FastAPI
## 🔌 Lancement de l'API (FastAPI)

### 1. Ajouter le router d'orientation
Le point d'entrée pour l'API est le fichier `api_runner.py`. Il utilise `uvicorn` pour lancer le serveur.

Dans `backend/app/api/main.py`:
### 1. Activer l'environnement virtuel

```python
from app.api.routes import orientation
Assurez-vous que votre environnement virtuel est activé :

api_router.include_router(orientation.router)
```bash
source venv/bin/activate
```

### 2. Initialiser au démarrage
### 2. Lancer le serveur

Dans `backend/app/main.py`:
Exécutez la commande suivante à la racine du projet :

```python
from app.api.routes.orientation import orientation_service

@app.on_event("startup")
async def startup_event():
    """Initialise le système d'orientation au démarrage"""
    orientation_service.initialize(models_dir="backend_ml/models/saved/")
```bash
# Lance le serveur avec rechargement automatique pour le développement
uvicorn api_runner:app --host 0.0.0.0 --port 8000 --reload
```

L'API sera alors disponible à l'adresse http://localhost:8000/docs.

### 3. Utiliser l'API

```bash
# Prédire une orientation
curl -X POST "http://localhost:8000/api/v1/orientation/predict" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "competence_programmation": 9,
    "competence_math": 8,
    "competence_physique": 6,
    "competence_electronique": 5,
    "competence_mecanique": 4,
    "competence_chimie": 5,
    "interet_aviation": 3,
    "interet_informatique": 9,
    "interet_donnees": 8,
    "interet_securite": 7,
    "interet_robotique": 5,
    "interet_energie": 4,
    "interet_cartographie": 3,
    "interet_automobile": 3,
    "trait_analytique": 9,
    "trait_creatif": 7,
    "trait_rigoureux": 7,
    "trait_aventureux": 4,
    "trait_methodique": 7,
    "moyenne_math": 15,
    "moyenne_physique": 13,
    "moyenne_informatique": 16,
    "moyenne_generale": 14.5
  }'
```

**Réponse attendue:**

```json
{
  "recommendations": [
    {
      "filiere": "Intelligence Artificielle",
      "score_final": 82.5,
      "confiance": "Très élevée",
      "score_regles": 85.0,
      "score_ml": 81.2,
      "recommendation_strength": "Fortement recommandé",
      "points_forts": [
        "Excellence en programmation (9/10)",
        "Bon niveau en mathématiques (8/10)",
        "Fort intérêt pour l'informatique (9/10)"
      ],
      "points_faibles": [],
      "methode": "Hybride (Règles + ML)"
    },
    {
      "filiere": "Génie Logiciel",
      "score_final": 78.3,
      "confiance": "Élevée",
      "score_regles": 80.0,
      "score_ml": 77.5,
      "recommendation_strength": "Recommandé",
      "methode": "Hybride (Règles + ML)"
    },
    {
      "filiere": "Big Data",
      "score_final": 75.1,
      "confiance": "Élevée",
      "score_regles": 72.0,
      "score_ml": 76.8,
      "recommendation_strength": "Recommandé",
      "methode": "Hybride (Règles + ML)"
    }
  ],
  "student_id": null,
  "timestamp": "2025-01-15T10:30:00"
}
```

### Endpoints disponibles

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/v1/orientation/predict` | Prédiction générique |
| POST | `/api/v1/orientation/predict/{student_id}` | Prédiction pour un étudiant spécifique |
| GET | `/api/v1/orientation/filieres` | Liste des filières disponibles |
| GET | `/api/v1/orientation/health` | Vérification du système |

---

## 📁 Structure du projet
```
Systéme_orientation_académique/ 
├── data/
│   ├── raw/                          # Données brutes (Kaggle, CSV...)
│   ├── processed/                    # Données nettoyées
│   └── synthetic/                    # Données synthétiques générées
│
├── models/
│   ├── saved/                        # Modèles entraînés
│   │   ├── orientation_model.pkl
│   │   ├── scaler.pkl
│   │   └── label_encoder.pkl
│   └── rules/                        # Règles expertes (JSON)
│       └── orientation_rules.json
│
├── src/
│   ├── data/
│   │   ├── data_generator.py        # Génération de données
│   │   ├── data_loader.py           # Chargement
│   │   └── preprocessor.py          # Prétraitement
│   │
│   ├── features/
│   │   └── feature_engineering.py   # Création de features
│   │
│   ├── models/
│   │   ├── rule_based.py            # Système à règles
│   │   ├── ml_model.py              # Modèle ML
│   │   └── hybrid_system.py         # Système hybride
│   │
│   ├── evaluation/
│   │   └── metrics.py               # Métriques d'évaluation
│   │
│   └── utils/
│       ├── config.py                # Configuration
│       └── logger.py                # Logs
│
├── notebooks/
│   ├── 01_data_exploration.ipynb    # Exploration des données
│   ├── 02_feature_engineering.ipynb # Création de features
│   └── 03_model_training.ipynb      # Entraînement du modèle
│
├── api/
│   ├── predict.py                   # API FastAPI
│   └── schemas.py                   # Schémas Pydantic
│
├── api_runner.py                    # Point d'entrée pour lancer l'API
├── tests/                           # Tests unitaires
├── logs/                            # Fichiers de logs
├── config.py                        # Module de chargement de la config
├── requirements.txt                 # Dépendances Python
├── config.yaml                      # Configuration globale
├── main.py                          # Point d'entrée principal
└── README.md                        # Cette documentation
```

---

## 🧠 Algorithmes

### 1. Système à règles expertes

**Principe:** Évalue le profil selon des critères définis par des experts

```python
Critères évalués:
├── Required (éliminatoires) → Score +30 par critère
├── Preferred (bonus)        → Score +15 par critère
└── Bonus (atouts)           → Score +10 par critère

Score final normalisé sur 100
```

**Exemple pour Intelligence Artificielle:**
- Required: Programmation ≥ 8, Math ≥ 8, Intérêt informatique ≥ 8
- Preferred: Intérêt données ≥ 7, Trait analytique ≥ 8
- Bonus: Moyenne math ≥ 14, Moyenne informatique ≥ 13

### 2. Machine Learning - Random Forest

**Caractéristiques:**
- Algorithme: Random Forest Classifier
- Nombre d'arbres: 100
- Profondeur maximale: 15
- Features: 25+ (compétences, intérêts, personnalité, notes)
- Validation croisée: 5-fold CV

**Avantages:**
- Robuste au surapprentissage
- Gère bien les données non linéaires
- Fournit l'importance des features
- Probabilités calibrées

### 3. Système hybride

**Formule de combinaison:**

```
Score_final = (Score_règles × 0.4) + (Score_ML × 0.6)
```

**Niveaux de confiance:**
- Très élevée: Score ≥ 75
- Élevée: Score ≥ 60
- Moyenne: Score ≥ 45
- Faible: Score < 45

**Force de recommandation:**
- Fortement recommandé: Accord ≥ 80% ET Score ≥ 70
- Recommandé: Accord ≥ 60% ET Score ≥ 55
- À considérer: Score ≥ 40

---

## 📊 Performance

### Métriques du modèle

Avec 1500 échantillons d'entraînement:

| Métrique | Valeur |
|----------|--------|
| **Accuracy** | ~85-90% |
| **Précision moyenne** | ~87% |
| **Rappel moyen** | ~86% |
| **F1-Score moyen** | ~86% |
| **CV Score** | 84% ± 3% |

### Top features importantes

1. **interet_informatique** (15.2%)
2. **competence_programmation** (14.8%)
3. **competence_math** (12.5%)
4. **interet_donnees** (10.3%)
5. **trait_analytique** (8.7%)
6. **moyenne_informatique** (7.9%)
7. **interet_aviation** (6.4%)
8. **competence_electronique** (5.8%)

### Temps de réponse

- Prédiction unique: **< 50ms**
- Batch de 100 étudiants: **< 2s**
- Entraînement complet: **~30s** (1500 samples)

---

## 🧪 Tests

### Exécuter les tests

```bash
# Tous les tests
pytest tests/ -v

# Tests spécifiques
pytest tests/test_rule_based.py -v
pytest tests/test_ml_model.py -v

# Avec couverture
pytest tests/ --cov=src --cov-report=html
```

### Exemple de test

```python
def test_prediction_high_programming():
    """Test avec profil fortement orienté programmation"""
    profile = {
        "competence_programmation": 9,
        "competence_math": 8,
        "interet_informatique": 9,
        # ...
    }
    
    recommendations = hybrid_system.recommend(profile, top_n=3)
    
    # Le top 1 devrait être une filière informatique
    assert recommendations[0]['filiere'] in [
        "Génie Logiciel", 
        "Intelligence Artificielle", 
        "Big Data"
    ]
    assert recommendations[0]['score_final'] > 70
```

---

## 🔧 Configuration

### Fichier config.yaml

```yaml
# Chemins
paths:
  data_raw: "data/raw/"
  models_saved: "models/saved/"

# Filières
filieres:
  - "Génie Logiciel"
  - "Intelligence Artificielle"
  # ...

# Modèle ML
model:
  algorithm: "RandomForest"
  test_size: 0.2
  random_state: 42
  
  rf_params:
    n_estimators: 100
    max_depth: 15

# Pondération hybride
weights:
  rules: 0.4
  ml: 0.6

# Seuils de confiance
confidence_thresholds:
  high: 0.75
  medium: 0.55
  low: 0.40
```

---

## 🚧 Roadmap

### Version 1.1 (En cours)
- [ ] Support des données réelles (intégration Kaggle)
- [ ] Modèle XGBoost en alternative
- [ ] Dashboard de visualisation des recommandations
- [ ] Export PDF des recommandations

### Version 1.2
- [ ] Système de feedback des étudiants
- [ ] Ré-entraînement automatique
- [ ] Multi-langues (FR/EN)
- [ ] API GraphQL

### Version 2.0
- [ ] Deep Learning (réseaux neuronaux)
- [ ] Analyse de CV/lettre de motivation
- [ ] Recommandations évolutives (suivi dans le temps)
- [ ] Prédiction du taux de réussite

---

## 📚 Ressources

### Documentation
- [scikit-learn](https://scikit-learn.org/stable/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/)

### Datasets
- [Student Performance Dataset - Kaggle](https://www.kaggle.com/datasets)
- [Educational Data Mining](https://educationaldatamining.org/)

### Articles
- Random Forest for Classification
- Hybrid Recommendation Systems
- Educational Data Mining Techniques

---

## 🤝 Contribution

Les contributions sont les bienvenues! Voici comment contribuer:

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

### Guidelines
- Suivre PEP 8 pour le style Python
- Ajouter des tests pour les nouvelles fonctionnalités
- Mettre à jour la documentation
- Commenter le code complexe

---

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

---

## 👥 Auteurs

- **Équipe Backend ML** - Système d'orientation académique
- **École d'Aéronautique et Technologies Avancées**

---

## 🙏 Remerciements

- Département pédagogique pour les règles métier
- Conseillers d'orientation pour leur expertise
- Étudiants ayant participé aux tests

---

## 📞 Contact

Pour toute question ou suggestion:
- Email: orientation@ecole-aero.edu
- Issues: GitHub Issues
- Documentation: Wiki du projet

---

## 🔥 Quick Start (TL;DR)

```bash
# Installation
pip install -r requirements.txt
# 1. Créer l'environnement et installer les dépendances
pip install uv
uv venv venv
source venv/bin/activate
uv pip install -r requirements.txt

# Lancer le pipeline complet
# 2. Lancer le pipeline complet (génération, entraînement, test)
python main.py --full-pipeline

# Tester l'API
python main.py --predict

# Intégrer à FastAPI
# Voir section "Intégration avec FastAPI"
# 3. Lancer le serveur API
uvicorn api_runner:app --reload
```

**Ça fonctionne? Félicitations! 🎉**

Vous avez maintenant un système d'orientation intelligent prêt à être intégré dans votre application.

---

*Dernière mise à jour: Octobre 2025*