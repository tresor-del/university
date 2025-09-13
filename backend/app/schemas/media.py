from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class MediaBase(BaseModel):
    id: int
    file_path: str 
    file_type: str
    mime_type: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class MediaResponse(MediaBase):
    pass

class MediaCreate(MediaBase):
    pass

class MediaResponse(BaseModel):
    data: List[MediaResponse]
    count: int

    model_config = ConfigDict(from_attributes=True)