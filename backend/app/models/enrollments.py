from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.core.config import Base

class Semester(Base):
    __tablename__ = "semesters"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # ex: "Semestre 1"

    enrollments = relationship("Enrollment", back_populates="semester")
    


class Enrollment(Base):
    __tablename__ = "enrollment"
    
    id = Column(Integer, primary_key=True, index=True, nullable=True)

    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("course.id"), nullable=False)
    semester_id = Column(Integer, ForeignKey("semesters.id"), nullable=True)
    
    student = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
    semester = relationship("Semester", back_populates="enrollments")
    