import enum

from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.core.config import Base

class UserRole(enum.Enum):
    ADMIN = "admin"
    STUDENT = "student"
    TEACHER = "teacher"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), index=True, nullable=False)
    full_name = Column(String(255), index=True, nullable=True)
    is_active = Column(Boolean, index=True)
    is_superuser = Column(Boolean, index=True)
    hashed_password = Column(String(128), index=True, nullable=False)

    student_id = Column(Integer,ForeignKey("etudiants.id") ,nullable=True)
    teacher_id = Column(Integer,ForeignKey("teachers.id") ,nullable=True)
    
    student = relationship("Student", back_populates="user", uselist=False)
    teacher = relationship("Teacher", back_populates="teacher", uselist=False)
    tokens = relationship("Token", back_populates="user", cascade="all, delete-orphan")
