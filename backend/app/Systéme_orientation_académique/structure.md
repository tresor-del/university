"""
========================================================================
BACKEND ML - SYSTÈME D'ORIENTATION ACADÉMIQUE
École d'Aéronautique et Technologies Avancées
========================================================================

Ce projet implémente un système hybride d'orientation académique combinant :
- Règles métier expertes
- Machine Learning (Random Forest, XGBoost)
- Scoring pondéré multi-critères

Structure du projet Backend ML - Système d'Orientation Académique
École d'Aéronautique et Technologies Avancées

backend_ml/
│
├── data/
│   ├── raw/                          # Données brutes
│   │   └── student_responses.csv     # Réponses des étudiants
│   ├── processed/                    # Données nettoyées
│   │   └── features_engineered.csv
│   └── synthetic/                    # Données synthétiques pour tests
│       └── generated_data.csv
│
├── models/
│   ├── saved/                        # Modèles entraînés
│   │   ├── orientation_model.pkl
│   │   ├── scaler.pkl
│   │   └── label_encoder.pkl
│   └── rules/                        # Règles métier
│       └── orientation_rules.json
│
├── src/
│   ├── __init__.py
│   │
│   ├── data/
│   │   ├── __init__.py
│   │   ├── data_generator.py        # Génération de données synthétiques
│   │   ├── data_loader.py           # Chargement des données
│   │   └── preprocessor.py          # Prétraitement
│   │
│   ├── features/
│   │   ├── __init__.py
│   │   └── feature_engineering.py   # Création de features
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── rule_based.py            # Système à règles
│   │   ├── ml_model.py              # Modèle ML
│   │   └── hybrid_system.py         # Système hybride
│   │
│   ├── evaluation/
│   │   ├── __init__.py
│   │   └── metrics.py               # Métriques d'évaluation
│   │
│   └── utils/
│       ├── __init__.py
│       ├── config.py                # Configuration
│       └── logger.py                # Logging
│
├── notebooks/
│   ├── 01_data_exploration.ipynb    # Exploration des données
│   ├── 02_feature_engineering.ipynb # Création de features
│   └── 03_model_training.ipynb      # Entraînement du modèle
│
├── tests/
│   ├── __init__.py
│   ├── test_preprocessor.py
│   ├── test_rule_based.py
│   └── test_ml_model.py
│
├── scripts/
│   ├── train_model.py               # Script d'entraînement
│   ├── generate_data.py             # Génération de données
│   └── evaluate_model.py            # Évaluation
│
├── api/
│   ├── __init__.py
│   ├── predict.py                   # API de prédiction
│   └── schemas.py                   # Schémas Pydantic
│
├── requirements.txt                  # Dépendances Python
├── README.md                        # Documentation
├── main.py                          # Point d'entrée principal
└── config.yaml                      # Configuration globale

"""

# Filières disponibles dans l'école
FILIERES = [
    "Génie Logiciel",
    "Intelligence Artificielle",
    "Big Data",
    "Objets Connectés (IoT)",
    "Cybersécurité",
    "Robotique",
    "Aéronautique",
    "Pilotage",
    "Pétrochimie",
    "Topographie",
    "Maintenance Automobile",
]

# Catégories de questions du formulaire
CATEGORIES_QUESTIONS = {
    "competences_techniques": [
        "Programmation",
        "Mathématiques",
        "Physique",
        "Électronique",
        "Mécanique"
    ],
    "interets": [
        "Aviation",
        "Informatique",
        "Données",
        "Sécurité",
        "Robotique",
        "Énergie",
        "Cartographie"
    ],
    "traits_personnalite": [
        "Analytique",
        "Créatif",
        "Rigoureux",
        "Aventureux",
        "Méthodique"
    ],
    "objectifs_carriere": [
        "Développement logiciel",
        "Recherche",
        "Pilotage",
        "Ingénierie",
        "Consulting"
    ]
}