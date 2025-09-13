from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.core.config import Base

class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, index=True, primary_key=True, autoincrement=True)
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

class TeachCourse(Base):
    __tablename__ = "teach"
    
    id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    
    course_id = Column(Integer, ForeignKey("cours.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    
    course = relationship("Course", back_populates="teachers_assoc")
    teacher = relationship("Teacher", back_populates="courses_assoc")

    
    