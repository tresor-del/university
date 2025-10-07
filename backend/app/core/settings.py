import secrets

from typing import Annotated, Any, List

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field, MySQLDsn, BeforeValidator, AnyUrl

from pydantic_core import MultiHostUrl


def parse_cors(v: Any) -> List[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",") if v.split()]
    elif  isinstance(v, list | str):
        return v
    return ValueError(v)


class Settings(BaseSettings):
    
    model_config = SettingsConfigDict(
        env_file = '.env.dev',
        env_ignore_empty=True,
        extra = "ignore"
    )
    
    API_V1_STR: str = "/api/v1"
    FRONTEND_HOST: str = "https://localhost:5173"
    BACKEND_CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)] = []

    @computed_field
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [self.FRONTEND_HOST]
    
    
    SECRET_KEY: str = secrets.token_urlsafe(32)
    
    PROJECT_NAME: str = ""
    MYSQL_SERVER: str = ""
    MYSQL_PORT: int = 1
    MYSQL_USER: str = ""
    MYSQL_PASSWORD: str = ""
    MYSQL_DB: str = ""
    HUGGINGFACE_API_KEY: str = ""
    
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