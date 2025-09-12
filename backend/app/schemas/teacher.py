from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


# Teacher

class TeacherBase(BaseModel):
    nom: str
    prenom: str
    email: Optional[EmailStr] = None
    telephone: Optional[str] = None
    grade: str
    id_departement: Optional[int] = None
    user_id: Optional[int] = None


    model_config = ConfigDict(from_attributes=True)
    

class TeacherCreate(TeacherBase):
    pass



class TeacherUpdate(BaseModel):
    nom: Optional[str] = None
    prenom: Optional[str] = None
    email: Optional[EmailStr] = None
    telephone: Optional[str] = None
    grade: Optional[str] = None
    id_departement: Optional[int] = None
    user_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class TeacherResponse(TeacherBase):
    id: int

class TeachersResponse(BaseModel):
    data: list[TeacherResponse]
    count: int



# TeachCourse

class TeachCourseBase(BaseModel):
    course_id: int
    teacher_id: int

    model_config = ConfigDict(from_attributes=True)

class TeachCourseCreate(TeachCourseBase):
    pass


class TeachCourseUpdate(BaseModel):
    course_id: Optional[int] = None
    teacher_id: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)


class TeachCourseResponse(TeachCourseBase):
    id: int
