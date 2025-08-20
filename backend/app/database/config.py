from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# lien a modifier
DATABASE_URL = "mysql+pymysql://root:123tresor%40@localhost:3306/gestion_ecole"

# créer une connexion a la base de donnée
engine = create_engine(
    DATABASE_URL
)

# usine de session pour créer des connexions temporaires a la base de donnée a la demande
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# la base commune que toutes tes classes de modèles SQLAlchemy vont utiliser pour créer des tables 
Base = declarative_base()