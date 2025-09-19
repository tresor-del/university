import uuid
from sqlalchemy import UUID, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.config import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.teachers import Teacher

class Media(Base):
    __tablename__ = "media"
    
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)
    file_path = Column(String(255), nullable=False)   # chemin vers le fichier
    file_type = Column(String(50), nullable=False)    # ex: "photo", "qr", "document"
    mime_type = Column(String(50), nullable=True)     # ex: "image/png", "image/jpeg"
    is_principal = Column(Boolean, nullable=True, default=False)
    
    student_id = Column(UUID(as_uuid=True), ForeignKey("etudiants.id"), nullable=True)
    teacher_id = Column(UUID(as_uuid=True), ForeignKey("teachers.id"), nullable=True)
    
    student = relationship("Student", back_populates="medias")
    teacher = relationship("Teacher", back_populates="medias")