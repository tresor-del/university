from datetime import datetime
import uuid
from sqlalchemy import UUID, Column, String, Integer, Text, ForeignKey
from sqlalchemy import event
from sqlalchemy.orm import relationship

from app.core.config import Base

class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)
    id_teacher = Column(String(100), unique=True, index=True, nullable=False)
    nom = Column(String(100), index=True, nullable=False)
    prenom = Column(String(100), index=True, nullable=False)
    email = Column(String(30), index=True, nullable=True)
    telephone = Column(String(30), index=True, nullable=True)
    grade = Column(String(50), index=True, nullable=False)
    
    id_departement = Column(Integer, ForeignKey("departements.id"), nullable=True)
    # user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    departement = relationship("Department", back_populates="teachers")
    user = relationship("User", back_populates="teacher")
    courses_assoc = relationship("TeachCourse", back_populates="teacher")
    medias = relationship("Media", back_populates="teacher")
    
@event.listens_for(Teacher, "before_insert")
def generer_id_etudiant(mapper, connection, target):
    if not target.id_teacher:
        target.id_teacher = f"TCH{datetime.now().year}-{uuid.uuid4().hex[:5]}"
    pass

class TeachCourse(Base):
    __tablename__ = "teach"
    
    id = Column(Integer, index=True, primary_key=True)
    
    course_id = Column(Integer, ForeignKey("cours.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    
    course = relationship("Course", back_populates="teachers_assoc")
    teacher = relationship("Teacher", back_populates="courses_assoc")

    
    