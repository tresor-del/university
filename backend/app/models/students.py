import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

from sqlalchemy import event

Base = declarative_base()

class Etudiant(Base):
    __tablename__ = "etudiants"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_etudiant = Column(String(50), unique=True, index=True, nullable=False)
    nom = Column(String, index=True, nullable=False)
    prenom = Column(String, index=True, nullable=False)
    sexe = Column(String, index=True, nullable=False)
    date_creation = Column(DateTime(timezone=True), server_default=func.now() ) 


# Générer l'identifiant de l'étudiant avant de l'ajouter
@event.listens_for(Etudiant, "before_insert")
def generer_id_etudiant(mapper, connection, target):
    if not target.id_etudiant:
        target.id_etudiant = f"STD{datetime.now().year}-{uuid.uuid4().hex[:8]}"
    pass
