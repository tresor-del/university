"""
Point d'entrée principal du système d'orientation académique
Pipeline complet: génération de données → entraînement → prédiction
"""
import os
import argparse
import sys
import pandas as pd
import yaml
from pathlib import Path

class OrientationPipeline:
    """Pipeline complet du système d'orientation"""
    
    def __init__(self):
        with open("config.yaml", "r") as f:
            self.config = yaml.safe_load(f)
        
        self.paths = self.config['paths']
        self.files = self.config['files']
        self._setup_directories()
    
    def _setup_directories(self):
        """Crée la structure de répertoires"""
        dirs = [
            self.paths['data_raw'], self.paths['data_processed'], self.paths['data_synthetic'],
            self.paths['models_saved'], self.paths['rules'],
            self.paths['logs']
        ]
        for d in dirs:
            os.makedirs(d, exist_ok=True)
    
    def generate_data(self, n_samples: int = 1500):
        """Étape 1: Génération de données synthétiques"""
        print("\n" + "="*70)
        print("ÉTAPE 1: GÉNÉRATION DE DONNÉES SYNTHÉTIQUES")
        print("="*70)
        
        from src.data.data_generator import generate_and_save_data
        
        output_path = os.path.join(self.paths['data_synthetic'], self.files['generated_data'])
        df = generate_and_save_data(output_path, n_samples=n_samples)
        
        print(f"\n📊 Statistiques des données:")
        print(f"  - Total d'échantillons: {len(df)}")
        print(f"  - Nombre de features: {len(df.columns) - 1}")
        print(f"  - Filières uniques: {df['filiere_cible'].nunique()}")
        
        print(f"\n📈 Distribution des filières:")
        dist = df['filiere_cible'].value_counts()
        for filiere, count in dist.items():
            print(f"  - {filiere}: {count} ({count/len(df)*100:.1f}%)")
        
        return df
    
    def train_model(self, data_path: str = None):
        """Étape 2: Entraînement du modèle ML"""
        print("\n" + "="*70)
        print("ÉTAPE 2: ENTRAÎNEMENT DU MODÈLE MACHINE LEARNING")
        print("="*70)
        
        from src.models.ml_model import OrientationMLModel
        
        if data_path is None:
            data_path = os.path.join(self.paths['data_synthetic'], self.files['generated_data'])
        
        # Vérifier que les données existent
        if not os.path.exists(data_path):
            raise FileNotFoundError(
                f"Fichier de données introuvable: {data_path}\n"
                "Exécutez d'abord: python main.py --generate-data"
            )
        
        # Charger les données
        print(f"\n📂 Chargement des données depuis {data_path}")
        df = pd.read_csv(data_path)
        print(f"✓ {len(df)} échantillons chargés")
        
        # Créer et entraîner le modèle
        model = OrientationMLModel(model_type="RandomForest")
        X, y = model.prepare_features(df)

        results = model.train(X, y, test_size=0.2, random_state=42)
        
        # Afficher les résultats
        print(f"\n📊 Performance du modèle:")
        print(f"  - Accuracy: {results['accuracy']:.3f}")
        print(f"  - CV Score: {results['cv_scores'].mean():.3f} (+/- {results['cv_scores'].std():.3f})")
        
        print(f"\n🎯 Top 10 features importantes:")
        print(results['feature_importance'].head(10).to_string(index=False))
        
        # Sauvegarder le modèle
        save_dir = self.paths['models_saved']
        model.save(
            model_path=os.path.join(save_dir, self.files['model']),
            scaler_path=os.path.join(save_dir, self.files['scaler']),
            encoder_path=os.path.join(save_dir, self.files['encoder'])
        )
        
        return model, results
    
    def test_prediction(self, student_profile: dict = None):
        """Étape 3: Test de prédiction"""
        print("\n" + "="*70)
        print("ÉTAPE 3: TEST DE PRÉDICTION")
        print("="*70)
        
        from src.models.rule_based import RuleBasedOrientationSystem
        from src.models.ml_model import OrientationMLModel
        from src.models.hybrid_system import HybridOrientationSystem
        
        # Profil de test par défaut
        if student_profile is None:
            student_profile = {
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
            }
        
        print("\n👤 Profil de l'étudiant testé:")
        print(f"  - Programmation: {student_profile['competence_programmation']}/10")
        print(f"  - Mathématiques: {student_profile['competence_math']}/10")
        print(f"  - Intérêt informatique: {student_profile['interet_informatique']}/10")
        print(f"  - Intérêt données: {student_profile['interet_donnees']}/10")
        print(f"  - Moyenne informatique: {student_profile['moyenne_informatique']}/20")
        
        # 1. Système à règles
        print("\n" + "-"*70)
        print("MÉTHODE 1: SYSTÈME À RÈGLES EXPERTES")
        print("-"*70)
        rules_path = os.path.join(self.paths['rules'], self.files['rules'])
        rule_system = RuleBasedOrientationSystem(rules_path=rules_path)
        rules_recs = rule_system.recommend(student_profile, top_n=3)
        
        for i, rec in enumerate(rules_recs, 1):
            print(f"\n{i}. {rec['filiere']}")
            print(f"   Score: {rec['score']}/100")
            print(f"   Confiance: {rec['confidence']}")
            print(f"   Raison: {rec['raison']}")
        
        # 2. Modèle ML
        print("\n" + "-"*70)
        print("MÉTHODE 2: MACHINE LEARNING")
        print("-"*70)
        
        ml_model = OrientationMLModel()
        try:
            ml_model.load(
                os.path.join(self.paths['models_saved'], self.files['model']),
                os.path.join(self.paths['models_saved'], self.files['scaler']),
                os.path.join(self.paths['models_saved'], self.files['encoder'])
            )
            
            ml_recs = ml_model.predict(student_profile)
            
            for i, rec in enumerate(ml_recs, 1):
                print(f"\n{i}. {rec['filiere']}")
                print(f"   Confiance: {rec['confidence']}%")
                print(f"   Niveau: {rec['confidence_label']}")
        
        except FileNotFoundError:
            print("⚠️  Modèle ML non trouvé. Exécutez d'abord: python main.py --train")
            ml_model = None
        
        # 3. Système hybride
        if ml_model and ml_model.is_trained:
            print("\n" + "-"*70)
            print("MÉTHODE 3: SYSTÈME HYBRIDE (RECOMMANDÉ)")
            print("-"*70)
            
            hybrid = HybridOrientationSystem(
                rule_system, ml_model,
                weights=self.config['weights']
            )
            hybrid_recs = hybrid.recommend(student_profile, top_n=3)
            
            for i, rec in enumerate(hybrid_recs, 1):
                print(f"\n{'='*60}")
                print(f"{i}. {rec['filiere']}")
                print(f"{'='*60}")
                print(f"Score final: {rec['score_final']}/100")
                print(f"Confiance: {rec['confiance']}")
                print(f"Recommandation: {rec['recommendation_strength']}")
                print(f"\nDétails:")
                print(f"  • Score règles: {rec['score_regles']}/100")
                print(f"  • Score ML: {rec['score_ml']}/100")
                
                # Explication détaillée pour la première recommandation
                if rec.get('points_forts'):
                    print(f"\n✓ Points forts:")
                    for strength in rec['points_forts']:
                        print(f"  • {strength}")
                if rec.get('points_faibles'):
                    print(f"\n⚠ Points à améliorer:")
                    for weakness in rec['points_faibles']:
                        print(f"  • {weakness}")
    
    def run_full_pipeline(self, n_samples: int = 1500):
        """Exécute le pipeline complet"""
        print("\n" + "="*70)
        print("🚀 PIPELINE COMPLET - SYSTÈME D'ORIENTATION ACADÉMIQUE")
        print("="*70)
        
        # Étape 1: Génération de données
        self.generate_data(n_samples=n_samples)
        
        # Étape 2: Entraînement
        self.train_model()
        
        # Étape 3: Test
        self.test_prediction()
        
        print("\n" + "="*70)
        print("✓ PIPELINE TERMINÉ AVEC SUCCÈS")
        print("="*70)
        print("\n💡 Prochaines étapes:")
        print("  1. Intégrer l'API de prédiction à votre backend FastAPI")
        print("  2. Tester avec de vrais profils d'étudiants")
        print("  3. Affiner les règles selon les retours terrain")
        print("  4. Ré-entraîner le modèle avec de vraies données")


def main():
    """Fonction principale avec CLI"""
    parser = argparse.ArgumentParser(
        description="Système d'orientation académique - École d'Aéronautique"
    )
    
    parser.add_argument(
        '--generate-data',
        action='store_true',
        help='Génère des données synthétiques'
    )
    
    parser.add_argument(
        '--train',
        action='store_true',
        help='Entraîne le modèle ML'
    )
    
    parser.add_argument(
        '--predict',
        action='store_true',
        help='Teste la prédiction'
    )
    
    parser.add_argument(
        '--full-pipeline',
        action='store_true',
        help='Exécute le pipeline complet'
    )
    
    parser.add_argument(
        '--n-samples',
        type=int,
        default=1500,
        help='Nombre d\'échantillons à générer (défaut: 1500)'
    )
    
    args = parser.parse_args()
    
    pipeline = OrientationPipeline()
    
    # Si aucun argument, exécuter le pipeline complet
    if not any([args.generate_data, args.train, args.predict, args.full_pipeline]):
        args.full_pipeline = True
    
    try:
        if args.full_pipeline:
            pipeline.run_full_pipeline(n_samples=args.n_samples)
        else:
            if args.generate_data:
                pipeline.generate_data(n_samples=args.n_samples)
            
            if args.train:
                pipeline.train_model()
            
            if args.predict:
                pipeline.test_prediction()
        
        print("\n✅ Terminé avec succès!\n")
        
    except Exception as e:
        print(f"\n❌ Erreur: {str(e)}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()