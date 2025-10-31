import uuid
from sqlalchemy import UUID, Column, String, Integer, Text, ForeignKey, Float, Boolean, Date
from sqlalchemy.orm import relationship

from app.core.config import Base
from app.models.university import Course


class Enrollment(Base):
    """
    Inscription d'un étudiant pour une année académique spécifique
    Un étudiant peut avoir plusieurs enrollments (un par année)
    """
    __tablename__ = "inscriptions"
    
    id = Column(Integer, primary_key=True)
    student_id = Column(UUID(as_uuid=True), ForeignKey("etudiants.id"), nullable=False)
    
    # Année académique
    annee_academique = Column(String(20), nullable=False) 
    
    # Niveau pour cette année
    niveau = Column(String(50), nullable=False)  # L1, L2, L3, M1, M2
    semestre = Column(Integer, nullable=True)  # 1 ou 2
    
    # Parcours pour cette année (peut changer)
    id_departement = Column(Integer, ForeignKey("departements.id"), nullable=False)
    id_parcours = Column(Integer, ForeignKey("parcours.id"), nullable=False)
    
    # Dates
    date_inscription = Column(Date, nullable=False)
    date_validation = Column(Date, nullable=True)
    
    # Statut de l'inscription
    statut = Column(String(50), default="en_cours")  # en_cours, validée, échouée, abandonnée
    
    # Résultats
    moyenne_annuelle = Column(Float, nullable=True)
    credits_obtenus = Column(Integer, default=0)
    est_admis = Column(Boolean, nullable=True)  # Admis en année supérieure ?
    
    # Relations
    student = relationship("Student", back_populates="enrollments")
    departement = relationship("Department")
    parcours = relationship("Program")