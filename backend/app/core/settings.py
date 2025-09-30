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
    
    PROJECT_NAME: str = ""
    MYSQL_SERVER: str = ""
    MYSQL_PORT: int = 1
    MYSQL_USER: str = ""
    MYSQL_PASSWORD: str = ""
    MYSQL_DB: str = ""
    HUGGINGFACE_API_KEY: str 
    
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
    FIRST_SUPERUSER: str = ""
    FIRST_SUPERUSER_PASSWORD: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    USERNAME_TEST_USER: str = ""
    MEDIA_UPLOAD_DIRE: str = ""

settings = Settings()