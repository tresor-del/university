from pydantic_settings import BaseSettings

from typing import List
from functools import lru_cache

# validation des variables récuperé depuis le fichier .env
class Settings(BaseSettings):
    host: str ="127.0.0.1"
    user: str ="root"
    password: str ="123tresor@"
    database: str ="esat_2"

    class Config:
        env_file = '.env'


# Mettre les parametres en cache pour eviter de lire le fichier a chaque requete
@lru_cache()
def get_settings():
    return Settings()