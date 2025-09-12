from pydantic import BaseModel, ConfigDict
from typing import Optional


# Semester

class SemesterBase(BaseModel):
    name: str 

    model_config = ConfigDict(from_attributes=True)
    
class SemesterCreate(SemesterBase):
    pass

class SemesterUpdate(BaseModel):
    name: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class SemesterResponse(SemesterBase):
    id: int



# Enrollment

class EnrollmentBase(BaseModel):
    student_id: int
    course_id: int
    semester_id: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentUpdate(BaseModel):
    student_id: Optional[int] = None
    course_id: Optional[int] = None
    semester_id: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)

class EnrollmentResponse(EnrollmentBase):
    id: int
    
