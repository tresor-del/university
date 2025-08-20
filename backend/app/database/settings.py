"""
Fichier non utilisé
"""
from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache

# validation des variables récuperé depuis le fichier .env
class Settings(BaseSettings):
    databaseurl: str = "mysql+pymysql://root:123tresor%40@localhost:3306/gestion_ecole"

    class Config:
        env_file = '../.env'


# Mettre les parametres en cache pour eviter de lire le fichier a chaque requete
@lru_cache()
def get_settings():
    return Settings()