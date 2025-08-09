from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    host: str
    user: str
    password: str
    database: str

    class Config:
        env_file = '.env'

# Mettre les parametres en cache pour eviter de lire le fichier a chaque requete
@lru_cache()
def get_settings():
    return Settings()