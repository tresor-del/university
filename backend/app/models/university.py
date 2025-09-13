from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.core.config import Base



class Course(Base):
    __tablename__ = "cours"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String(155), index=True, nullable=False)
    titre = Column(String(155), index=True, nullable=False)
    description = Column(Text, nullable=True)
    credits = Column(Integer, index=True, nullable=False)

    id_parcours = Column(Integer, ForeignKey("parcours.id"), nullable=False)
    
    parcours = relationship("Program", back_populates="courses")
    enrollments = relationship("Enrollment", back_populates="courses")
    teachers_assoc = relationship("TeachCourse", back_populates="course")

# Parcours/Filière
class Program(Base):
    __tablename__ = "parcours"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nom = Column(String(255), index=True, nullable=False)
    niveau = Column(String(255), index=True, nullable=False)
    duree = Column(Integer, index=True, nullable=False)
    
    id_departement = Column(Integer, ForeignKey("departements.id"), nullable=False)
    
    departement = relationship("Department", back_populates="programs")
    students = relationship("Student", back_populates="parcours")
    courses = relationship("Course", back_populates="parcours")

class Department(Base):
    __tablename__ = "departements"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nom = Column(String(155), index=True, nullable=False)
    description = Column(Text, nullable=True)
    
    id_faculte = Column(Integer, ForeignKey("facultés.id"), nullable=False)
    
    faculte = relationship("Faculty", back_populates="departements")
    students = relationship("Student", back_populates="departement")
    programs = relationship("Program", back_populates="departement")
    teachers = relationship("Teacher", back_populates="departement")

class Faculty(Base):
    __tablename__ = "facultés"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nom = Column(String(155), index=True, nullable=False)
    description = Column(Text, nullable=True)

    departements = relationship("Department", back_populates="faculte")
    