from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.config import Base

class Media(Base):
    __tablename__ = "media"
    
    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String(255), nullable=False)   # chemin vers le fichier
    file_type = Column(String(50), nullable=False)    # ex: "photo", "qr", "document"
    mime_type = Column(String(50), nullable=True)     # ex: "image/png", "image/jpeg"
    
    student_id = Column(Integer, ForeignKey("etudiants.id"), nullable=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=True)
    
    student = relationship("Student", back_populates="medias")
    teacher = relationship("Teacher", back_populates="medias")