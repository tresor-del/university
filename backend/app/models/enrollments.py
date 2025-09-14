import uuid
from sqlalchemy import UUID, Column, String, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.core.config import Base
from app.models.university import Course

class Semester(Base):
    __tablename__ = "semesters"
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)
    name = Column(String(50), nullable=False)  # ex: "Semestre 1"

    enrollments = relationship("Enrollment", back_populates="semester")
    


class Enrollment(Base):
    __tablename__ = "enrollment"
    
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)

    student_id = Column(Integer, ForeignKey("etudiants.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("cours.id"), nullable=False) 
    semester_id = Column(Integer, ForeignKey("semesters.id"), nullable=True)
    
    student = relationship("Student", back_populates="enrollments")
    courses = relationship("Course", back_populates="enrollments")
    semester = relationship("Semester", back_populates="enrollments")
    