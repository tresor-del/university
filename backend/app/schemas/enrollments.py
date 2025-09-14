from pydantic import BaseModel, ConfigDict
from typing import Optional

from uuid import UUID


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
    id: UUID



# Enrollment

class EnrollmentBase(BaseModel):
    student_id: UUID
    course_id: UUID
    semester_id: Optional[UUID] = None
    
    model_config = ConfigDict(from_attributes=True)

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentUpdate(BaseModel):
    student_id: Optional[UUID] = None
    course_id: Optional[UUID] = None
    semester_id: Optional[UUID] = None
    
    model_config = ConfigDict(from_attributes=True)

class EnrollmentResponse(EnrollmentBase):
    id: UUID
    
