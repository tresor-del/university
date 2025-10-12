"""
Point d'entrée pour lancer le serveur API FastAPI avec Uvicorn.

Ce fichier est distinct du `main.py` qui gère le pipeline ML.
"""
from fastapi import FastAPI
import uvicorn

# Importe le routeur depuis votre module de prédiction
from api.predict import router as orientation_router
from api.predict import get_orientation_service

app = FastAPI(
    title="Système d'Orientation Académique API",
    description="API pour le système d'orientation hybride combinant règles métier et Machine Learning.",
    version="1.0.1",
)

# Inclure le routeur des prédictions
app.include_router(orientation_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    """Initialise le service d'orientation au démarrage de l'application."""
    print("🚀 Démarrage de l'application et initialisation du service...")
    try:
        get_orientation_service()  # Appelle la fonction pour initialiser et mettre en cache le service
        print("✓ Service initialisé et prêt à recevoir des requêtes.")
    except Exception as e:
        print(f"🔥 Échec critique de l'initialisation du service: {e}")

if __name__ == "__main__":
    uvicorn.run("api_runner:app", host="0.0.0.0", port=8000, reload=True)