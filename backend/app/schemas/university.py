from pydantic import BaseModel, ConfigDict
from typing import Optional, List


# Faculty

class FacultyBase(BaseModel):
    nom: str
    description: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class FacultyCreate(FacultyBase):
    pass

class FacultyUpdate(BaseModel):
    nom: Optional[str] = None
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
    

class FacultyResponse(FacultyBase):
    id: int

class FacultiesResponse(BaseModel):
    data: List[FacultyResponse] = None
    count: int
    
    model_config = ConfigDict(from_attributes=True)

# Department

class DepartmentBase(BaseModel):
    nom: str
    description: Optional[str] = None
    id_faculte: int

    model_config = ConfigDict(from_attributes=True)

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(BaseModel):
    nom: Optional[str] = None
    description: Optional[str] = None
    id_faculte: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)

class DepartmentResponse(DepartmentBase):
    id: int
    faculte: Optional[FacultyResponse] = None  # relation

class DepartementsResponse(BaseModel):
    data: List[FacultyResponse] = None
    count: int
    
    model_config = ConfigDict(from_attributes=True)


# Program

class ProgramBase(BaseModel):
    nom: str
    niveau: str
    duree: int
    id_departement: int
    
    model_config = ConfigDict(from_attributes=True)

class ProgramCreate(ProgramBase):
    pass

class ProgramUpdate(BaseModel):
    nom: Optional[str] = None
    niveau: Optional[str] = None
    duree: Optional[int] = None
    id_departement: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)

class ProgramResponse(ProgramBase):
    id: int
    departement: Optional[DepartmentResponse] = None  # relation

    model_config = ConfigDict(from_attributes=True)

class ProgramsResponse(BaseModel):
    data: List[ProgramResponse] = None
    count: int
    
    model_config = ConfigDict(from_attributes=True)

# Course

class CourseBase(BaseModel):
    code: str
    titre: str
    description: Optional[str] = None
    credits: int
    id_parcours: int

    model_config = ConfigDict(from_attributes=True)
    
class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    code: Optional[str] = None
    titre: Optional[str] = None
    description: Optional[str] = None
    credits: Optional[int] = None
    id_parcours: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)

class CourseResponse(CourseBase):
    id: int
    parcours: Optional[ProgramResponse] = None 

    model_config = ConfigDict(from_attributes=True)

class CoursesResponse(BaseModel):
    data: List[CourseResponse] = None
    count: int
    
    model_config = ConfigDict(from_attributes=True)