import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# from .settings import get_settings

# settings = get_settings()

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


# créer une connexion a la base de donnée
engine = create_engine(
    DATABASE_URL
)

# usine de session pour créer des connexions temporaires a la base de donnée a la demande
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

