from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

from uuid import UUID


# Teacher

class TeacherBase(BaseModel):
    id_teacher: str
    nom: str
    prenom: str
    email: Optional[EmailStr] = None
    telephone: Optional[str] = None
    grade: str

    model_config = ConfigDict(from_attributes=True)
    

class TeacherCreate(TeacherBase):
    pass


class TeacherUpdate(BaseModel):
    nom: Optional[str] = None
    prenom: Optional[str] = None
    email: Optional[EmailStr] = None
    telephone: Optional[str] = None
    grade: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class TeacherResponse(TeacherBase):
    id: UUID

class TeachersResponse(BaseModel):
    data: list[TeacherResponse]
    count: int



# TeachCourse

class TeachCourseBase(BaseModel):
    course_id: UUID
    teacher_id: UUID

    model_config = ConfigDict(from_attributes=True)

class TeachCourseCreate(TeachCourseBase):
    pass


class TeachCourseUpdate(BaseModel):
    course_id: Optional[UUID] = None
    teacher_id: Optional[UUID] = None
    
    model_config = ConfigDict(from_attributes=True)


class TeachCourseResponse(TeachCourseBase):
    id: UUID
