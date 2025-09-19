from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List, Optional

from uuid import UUID

from app.schemas.media import MediaResponse

# Teacher

class TeacherBase(BaseModel):
    nom: str
    prenom: str
    email: Optional[EmailStr] = None
    telephone: Optional[str] = None
    grade: str
    medias: Optional[list] = []
    
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
    id_teacher: str

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
