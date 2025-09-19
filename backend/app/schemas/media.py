from pydantic import BaseModel, ConfigDict
from typing import Optional, List

from uuid import UUID

class MediaBase(BaseModel):
    """
    Modèle de base
    """
    file_path: str = None
    file_type: str = None
    mime_type: Optional[str] = None
    teacher_id: Optional[UUID] = None
    student_id: Optional[UUID] = None
    is_principal: Optional[bool] = None
    
    model_config = ConfigDict(from_attributes=True)

class MediaResponse(BaseModel):
    """
    Modèle pour la réponse - tous les champs requis.
    """
    id: UUID
    file_path: str
    file_type: str
    mime_type: Optional[str] = None
    teacher_id: Optional[UUID] = None
    student_id: Optional[UUID] = None
    
    model_config = ConfigDict(from_attributes=True)

class MediaCreate(MediaBase):
    pass

class MediasResponse(BaseModel):
    data: List[MediaResponse]
    count: int

    model_config = ConfigDict(from_attributes=True)