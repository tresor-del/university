import uuid
from datetime import datetime

from sqlalchemy import UUID
from sqlalchemy import Column, Integer, String, DateTime, Date
from sqlalchemy.sql import func

from sqlalchemy import event
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.core.config import Base
from app.models.enrollments import Enrollment
from app.models.media import Media


class Student(Base):
    __tablename__ = "etudiants"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True, autoincrement=True)
    id_etudiant = Column(String(50), unique=True, index=True, nullable=False)
    nom = Column(String(100), index=True, nullable=False)
    prenom = Column(String(100), index=True, nullable=False)
    date_naissance = Column(Date, index=True, nullable=False)
    lieu_naissance = Column(String(100), index=True, nullable=False)
    sexe = Column(String(10), index=True, nullable=False)
    nationalite = Column(String(50), nullable=False)
    adresse = Column(String(255), nullable=True)
    email = Column(String(120), unique=True, index=True, nullable=False)
    telephone = Column(String(20), nullable=False)
    
    nom_du_pere = Column(String(100), nullable=False)
    nom_de_la_mere = Column(String(100), nullable=False)
    addresse_du_pere = Column(String(100), nullable=False)
    addresse_de_la_mere = Column(String(100), nullable=False)
    
    nom_parent_tuteur = Column(String(100), nullable=False)
    telephone_parent_tuteur = Column(String(20), nullable=False)
    adresse_parent_tuteur = Column(String(255), nullable=False)
    
    # photo = Column(String(255), nullable=True)
    date_inscription = Column(Date, server_default=func.current_date())
    statut = Column(String(50), default="actif")
    date_creation = Column(DateTime(timezone=True), server_default=func.now())
    # qr_path = Column(String(200))

    # id_user = Column(Integer, ForeignKey("users.id"), nullable=True)
    id_departement = Column(Integer, ForeignKey("departements.id"), nullable=True)
    id_parcours = Column(Integer, ForeignKey("parcours.id"), nullable=True)

    user = relationship("User", back_populates="student")
    departement = relationship("Department", back_populates="students")
    parcours = relationship("Program", back_populates="students")
    enrollments = relationship("Enrollment", back_populates="student")
    medias = relationship("Media", back_populates="student")

@event.listens_for(Student, "before_insert")
def generer_id_etudiant(mapper, connection, target):
    if not target.id_etudiant:
        target.id_etudiant = f"STD{datetime.now().year}-{uuid.uuid4().hex[:8]}"
    pass



