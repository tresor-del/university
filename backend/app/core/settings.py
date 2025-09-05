"""
Fichier non utilisé
"""
import secrets
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from functools import lru_cache
from pydantic import (
    computed_field,
    MySQLDsn
)
from pydantic_core import MultiHostUrl


# validation des variables récuperé depuis le fichier .env
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file = '../.env',
        env_ignore_empty=True,
    )
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    PROJECT_NAME: str = "Gestion Scolaire"
    MYSQL_SERVER: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "docker_user"
    MYSQL_PASSWORD: str = "votre_mot_de_passe"
    MYSQL_DB: str = "gestion_ecole"
    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> MySQLDsn:
        return MultiHostUrl.build(
            scheme="mysql+pymysql",
            username=self.MYSQL_USER,
            password=self.MYSQL_PASSWORD,
            host=self.MYSQL_SERVER,
            port=self.MYSQL_PORT,
            path=self.MYSQL_DB
        )
    FIRST_SUPERUSER: str = "tresor"
    FIRST_SUPERUSER_PASSWORD: str = "tresoradmainpasse"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    USERNAME_TEST_USER: str = "tresortest"

settings = Settings()