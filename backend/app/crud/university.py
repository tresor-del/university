from pydantic import BaseModel
from typing import Optional, List


# =====================
# Faculty
# =====================
class FacultyBase(BaseModel):
    nom: str
    description: Optional[str] = None

class FacultyCreate(FacultyBase):
    pass

class FacultyUpdate(BaseModel):
    nom: Optional[str] = None
    description: Optional[str] = None

class FacultyResponse(FacultyBase):
    id: int

    class Config:
        orm_mode = True


# =====================
# Department
# =====================
class DepartmentBase(BaseModel):
    nom: str
    description: Optional[str] = None
    id_faculte: int

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(BaseModel):
    nom: Optional[str] = None
    description: Optional[str] = None
    id_faculte: Optional[int] = None

class DepartmentResponse(DepartmentBase):
    id: int
    faculte: Optional[FacultyResponse] = None  # relation

    class Config:
        orm_mode = True


# =====================
# Program
# =====================
class ProgramBase(BaseModel):
    nom: str
    niveau: str
    duree: int
    id_departement: int

class ProgramCreate(ProgramBase):
    pass

class ProgramUpdate(BaseModel):
    nom: Optional[str] = None
    niveau: Optional[str] = None
    duree: Optional[int] = None
    id_departement: Optional[int] = None

class ProgramResponse(ProgramBase):
    id: int
    departement: Optional[DepartmentResponse] = None  # relation

    class Config:
        orm_mode = True


# =====================
# Course
# =====================
class CourseBase(BaseModel):
    code: str
    titre: str
    description: Optional[str] = None
    credits: int
    id_parcours: int

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    code: Optional[str] = None
    titre: Optional[str] = None
    description: Optional[str] = None
    credits: Optional[int] = None
    id_parcours: Optional[int] = None

class CourseResponse(CourseBase):
    id: int
    parcours: Optional[ProgramResponse] = None  # relation

    class Config:
        orm_mode = True
