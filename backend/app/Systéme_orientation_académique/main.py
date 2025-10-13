"""
Point d'entrée principal pour le pipeline ML.
Permet de générer les données, entraîner le modèle et lancer des prédictions de test.
"""
import argparse
import os
import pandas as pd
from config import get_config
from src.data.data_generator import DataGenerator
from src.models.ml_model import OrientationMLModel
from src.models.rule_based import RuleBasedOrientationSystem
from src.models.hybrid_system import HybridOrientationSystem

def run_data_generation(config: dict, n_samples: int):
    """Génère des données synthétiques."""
    print(f"--- Génération de {n_samples} échantillons de données synthétiques ---")
    generator = DataGenerator(config['filieres'])
    df = generator.generate(n_samples)
    
    output_dir = config['paths']['data_synthetic']
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, config['files']['synthetic_data'])
    df.to_csv(output_path, index=False)
    print(f"✓ Données sauvegardées dans {output_path}")

def run_training(config: dict):
    """Entraîne le modèle de Machine Learning."""
    print("--- Entraînement du modèle ML ---")
    data_path = os.path.join(config['paths']['data_synthetic'], config['files']['synthetic_data'])
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print(f"❌ Fichier de données non trouvé: {data_path}")
        print("Veuillez d'abord générer les données avec --generate-data")
        return

    ml_model = OrientationMLModel(model_params=config['model']['rf_params'])
    X, y = ml_model.prepare_features(df)
    
    metrics = ml_model.train(X, y, test_size=config['model']['test_size'], random_state=config['model']['random_state'])
    print(f"✓ Entraînement terminé. Accuracy: {metrics['accuracy']:.2f}")

    # Sauvegarde des modèles
    models_dir = config['paths']['models_saved']
    os.makedirs(models_dir, exist_ok=True)
    ml_model.save(
        os.path.join(models_dir, config['files']['model']),
        os.path.join(models_dir, config['files']['scaler']),
        os.path.join(models_dir, config['files']['encoder'])
    )

def run_prediction_test(config: dict):
    """Exécute une prédiction de test avec le système hybride."""
    print("--- Test de prédiction avec le système hybride ---")
    # Initialiser les systèmes
    rules_path = os.path.join(config['paths']['rules'], config['files']['rules'])
    rule_system = RuleBasedOrientationSystem(rules_path=rules_path)
    
    ml_model = OrientationMLModel()
    models_dir = config['paths']['models_saved']
    ml_model.load(
        os.path.join(models_dir, config['files']['model']),
        os.path.join(models_dir, config['files']['scaler']),
        os.path.join(models_dir, config['files']['encoder'])
    )

    hybrid = HybridOrientationSystem(rule_system, ml_model, weights=config['weights'])

    # Profil étudiant de test
    student_profile = {
        "competence_programmation": 9, "competence_math": 8, "competence_physique": 6,
        "competence_electronique": 5, "competence_mecanique": 4, "competence_chimie": 5,
        "interet_aviation": 3, "interet_informatique": 9, "interet_donnees": 8,
        "interet_securite": 7, "interet_robotique": 5, "interet_energie": 4,
        "interet_cartographie": 3, "interet_automobile": 3, "trait_analytique": 9,
        "trait_creatif": 7, "trait_rigoureux": 7, "trait_aventureux": 4,
        "trait_methodique": 7, "moyenne_math": 15, "moyenne_physique": 13,
        "moyenne_informatique": 16, "moyenne_generale": 14.5
    }

    recommendations = hybrid.recommend(student_profile, top_n=3)
    print("Recommandations pour le profil de test :")
    for rec in recommendations:
        print(f"- {rec['filiere']}: Score final = {rec['score_final']:.2f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pipeline du système d'orientation.")
    parser.add_argument("--generate-data", action="store_true", help="Générer des données synthétiques.")
    parser.add_argument("--n-samples", type=int, default=1500, help="Nombre d'échantillons à générer.")
    parser.add_argument("--train", action="store_true", help="Entraîner le modèle ML.")
    parser.add_argument("--predict", action="store_true", help="Lancer une prédiction de test.")
    parser.add_argument("--full-pipeline", action="store_true", help="Exécuter la génération de données et l'entraînement.")
    args = parser.parse_args()

    config = get_config()

    if args.full_pipeline or args.generate_data:
        run_data_generation(config, args.n_samples)
    if args.full_pipeline or args.train:
        run_training(config)
    if args.predict:
        run_prediction_test(config)

    if not any(vars(args).values()):
        parser.print_help()