from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Etudiant(Base):
    __tablename__ = "Etudiant"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_etudiant = Column(Integer, unique=True, index=True, nullable=False)
    nom = Column(String, index=True, nullable=False)
    prenom = Column(String, index=True, nullable=False)
    sexe = Column(String, index=True, nullable=False)
    date_creation = Column(DateTime, default=datetime.utcnow)  
