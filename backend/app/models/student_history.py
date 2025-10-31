# app/models/student_history.py
import uuid
from sqlalchemy import Column, String, Date, DateTime, ForeignKey, Integer, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy import UUID
from app.core.config import Base
from sqlalchemy.sql import func

class StudentHistory(Base):
    """
    Table pour garder l'historique complet des inscriptions d'un étudiant
    """
    __tablename__ = "historique_etudiants"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(UUID(as_uuid=True), ForeignKey("etudiants.id"), nullable=False)
    
    # Informations de la période
    annee_academique = Column(String(20), nullable=False)  # ex: "2023-2024"
    date_debut = Column(Date, nullable=False)
    date_fin = Column(Date, nullable=True)
    
    # Statut et niveau
    statut = Column(String(50), nullable=False)  # actif, diplômé, abandon, etc.
    niveau = Column(String(100), nullable=True)  # L1, L2, M1, etc.
    id_departement = Column(Integer, ForeignKey("departements.id"), nullable=True)
    id_parcours = Column(Integer, ForeignKey("parcours.id"), nullable=True)
    
    # Détails de fin
    est_diplome = Column(Boolean, default=False)
    motif_fin = Column(Text, nullable=True)  # diplômé, abandon, transfert, suspension
    
    # Métadonnées
    date_creation = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(Text, nullable=True)  # Notes administratives
    
    # Relations
    student = relationship("Student", backref="historique")
    departement = relationship("Department")
    parcours = relationship("Program")