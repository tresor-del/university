"""
Modèle de Machine Learning pour la prédiction d'orientation.
"""
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from typing import Dict, Any, Tuple, List

class OrientationMLModel:
    """
    Encapsule le pipeline du modèle ML: préparation, entraînement, prédiction.
    """

    def __init__(self, model_type: str = "RandomForest", model_params: Dict = None):
        self.model_type = model_type
        self.model_params = model_params or {'n_estimators': 100, 'random_state': 42}
        self.model = None
        self.scaler = StandardScaler()
        self.encoder = LabelEncoder()
        self.is_trained = False
        self.features = []

    def prepare_features(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """Prépare les features et la cible à partir du DataFrame."""
        X = df.drop('filiere_cible', axis=1)
        y = df['filiere_cible']
        self.features = X.columns.tolist()
        return X, y

    def train(self, X: pd.DataFrame, y: pd.Series, test_size: float = 0.2, random_state: int = 42) -> Dict:
        """
        Entraîne le modèle, le scaler et l'encodeur.
        """
        # Encoder la cible
        y_encoded = self.encoder.fit_transform(y)

        # Diviser les données
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, test_size=test_size, random_state=random_state, stratify=y_encoded
        )

        # Normaliser les features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        # Initialiser et entraîner le modèle
        if self.model_type == "RandomForest":
            self.model = RandomForestClassifier(**self.model_params)
        else:
            raise ValueError(f"Type de modèle non supporté: {self.model_type}")

        self.model.fit(X_train_scaled, y_train)
        self.is_trained = True

        # Évaluation
        y_pred = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        cv_scores = cross_val_score(self.model, self.scaler.transform(X), y_encoded, cv=5)
        
        feature_importance = pd.DataFrame({
            'feature': self.features,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)

        return {
            "accuracy": accuracy,
            "cv_scores": cv_scores,
            "feature_importance": feature_importance
        }

    def predict(self, profile: Dict[str, Any], top_n: int = 3) -> List[Dict[str, Any]]:
        """
        Prédit les probabilités pour chaque filière pour un profil donné.
        """
        if not self.is_trained:
            raise RuntimeError("Le modèle n'est pas entraîné ou chargé.")

        # Créer un DataFrame à partir du profil
        profile_df = pd.DataFrame([profile], columns=self.features)
        
        # Normaliser le profil
        profile_scaled = self.scaler.transform(profile_df)

        # Prédire les probabilités
        probabilities = self.model.predict_proba(profile_scaled)[0]

        # Obtenir les top N prédictions
        top_indices = probabilities.argsort()[-top_n:][::-1]

        recommendations = []
        for i in top_indices:
            confidence = probabilities[i]
            recommendations.append({
                "filiere": self.encoder.classes_[i],
                "confidence": round(confidence * 100, 2),
                "confidence_label": "Élevée" if confidence > 0.7 else "Moyenne"
            })
        return recommendations

    def save(self, model_path: str, scaler_path: str, encoder_path: str):
        """Sauvegarde le modèle, le scaler et l'encodeur."""
        if not self.is_trained:
            raise RuntimeError("Impossible de sauvegarder un modèle non entraîné.")
        joblib.dump(self.model, model_path)
        joblib.dump(self.scaler, scaler_path)
        joblib.dump(self.encoder, encoder_path)
        print(f"✓ Modèle sauvegardé dans {model_path}")
        print(f"✓ Scaler sauvegardé dans {scaler_path}")
        print(f"✓ Encoder sauvegardé dans {encoder_path}")

    def load(self, model_path: str, scaler_path: str, encoder_path: str):
        """Charge un modèle, un scaler et un encodeur pré-entraînés."""
        try:
            self.model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
            self.encoder = joblib.load(encoder_path)
            
            # Récupérer les noms des features depuis le scaler
            if hasattr(self.scaler, 'feature_names_in_'):
                 self.features = self.scaler.feature_names_in_
            
            self.is_trained = True
            print("✓ Modèle, scaler et encoder chargés avec succès.")
        except FileNotFoundError as e:
            print(f"❌ Erreur de chargement: un fichier est manquant. {e}")
            raise